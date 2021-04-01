class Helper:

    def unpack_kwargs(self, kwargs: dict) -> str:
        """
        Function to format kwargs and translate the dictionary
        to be used to render the jinja template

        Args:
            kwargs (dict): Parameters packed in a python dictionary
                    ex: {'redshift_distkey': 'id', 'redshift_diststyle': 'KEY'}

        Returns:
            (str): ex: redshift_distkey='id',redshift_diststyle='KEY'
        """
        stmt = ','.join((f"{a}={b}" for a, b in kwargs.items()))
        return stmt
