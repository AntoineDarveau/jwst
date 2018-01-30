from . import model_base
from .image import ImageModel
from .slit import SlitModel, SlitDataModel


__all__ = ['MultiSlitModel']



class MultiSlitModel(model_base.DataModel):
    """
    A data model for multi-slit images.

    This model has a special member `slits` that can be used to
    deal with an entire slit at a time.  It behaves like a list::

       >>> multislit_model.slits.append(image_model)
       >>> multislit_model.slits[0]
       <ImageModel>

    If `init` is a file name or an `ImageModel` instance, an empty
    `ImageModel` will be created and assigned to attribute `slits[0]`,
    and the `data`, `dq`, `err`, and `relsens` attributes from the
    input file or `ImageModel` will be copied to the first element of
    `slits`.

    Parameters
    ----------
    init : any
        Any of the initializers supported by `~jwst.datamodels.DataModel`.
    """
    schema_url = "multislit.schema.yaml"

    def __init__(self, init=None, **kwargs):
        if isinstance(init, (SlitModel, ImageModel)):
            super(MultiSlitModel, self).__init__(init=None, **kwargs)
            self.update(init)
            self.slits.append(self.slits.item())
            self.slits[0].data = init.data
            self.slits[0].dq = init.dq
            self.slits[0].err = init.err
            self.slits[0].relsens = init.relsens
            self.slits[0].area = init.area
            self.slits[0].wavelength = init.wavelength
            return

        super(MultiSlitModel, self).__init__(init=init, **kwargs)

    def __getitem__(self, key):
        """
        Get a metadata value using a dotted name.
        """
        if isinstance(key, str) and key.split('.') == 'meta':
            super(MultiSlitModel, self).__getitem__(key)
        elif isinstance(key, int):
            # Return an instance of a SlitModel
            slit = self.slits[key]  # returns an ObjectNode instance
            #data_keys = [item[0] for item in slit.items() if not
                         ##item[0].startswith(("meta", "extra_fits"))]
                         #item[0].startswith("meta")]

            #kwargs = dict(((k, getattr(self.slits[key], k)) for k in data_keys))
            kwargs = {}
            items = dict(slit.items())
            for key in items:
                if not key.startswith(('meta', 'extra_fits')):
                    kwargs[key] = items[key]
            s = SlitModel(**kwargs)
            s.update(self)
            return s
        else:
            raise ValueError("Invalid key {0}".format(key))

    @property
    def slits(self):
        return self._slits

    @slits.setter
    def slits(self, val):
        return self._slits.extend(val)