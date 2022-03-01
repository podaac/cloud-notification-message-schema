import os
import json
import datetime


class CloudNotificationMessage:
    cnm_version: str
    granule: str
    collection: str
    files: list
    data_version: str
    provider: str
    trace: str
    product: dict

    def __init__(self, dataset, file_metadata, data_version, provider, cnm_version='1.5', granule_name=None, trace=None):
        """
        This class models a cloud notification message, 'submission' message.
        Adapted from NASA/JPL/PO.DAAC ingest and archive dev tools

        Parameters
        ----------
        dataset : str
            Short name of the dataset/collection
        file_metadata : list, dict
            A list of dictionaries, where each dictionary has the following:
                required attributes: uri (str), size (int), type (dict)
                optional attributes: subtype (dict) and checksum (str)
        data_version: str
            Version of the granule
        provider: str
            The name of the dataset provider
        cnm_version: str (optional)
            The cnm schema version for this CNM object, defaults to v1.5
        granule_name : str (optional)
            Name of the granule the CNM is constructed around, if not provided
            the data file name (without extension) is used
        """

        self.trace = trace
        self.cnm_version = cnm_version
        self.collection = dataset
        self.granule = granule_name
        self.files = file_metadata
        self.data_version = data_version
        self.provider = provider
        self.product = self.parse_files()

        # add data version to product if provided/specified
        if self.data_version is not None:
            self.product.update(dataVersion=self.data_version)

        # populate the bulk of the final message dict now
        self.message = dict(
            version=self.cnm_version,
            provider=self.provider,
            collection=self.collection,
            submissionTime=datetime.datetime.utcnow().isoformat(),
            identifier=self.granule,
            product=self.product
        )

        # If the user provided a trace field, add that to the message
        if self.trace is not None:
            self.message['trace'] = self.trace

    def parse_files(self):
        """
        Parses the 'file_metadata' input from the user, and builds the 'product' section

        Returns
        -------
        dict
            the 'product' section for the CNM submission object.
        """
        for file in self.files:
            file['name'] = os.path.basename(file['uri'])
            if file.get('checksum'):
                file['checksumType'] = 'md5'
                file.pop('checksum')
            if file.get('type') == 'data' and self.granule is None:
                self.granule, _ = os.path.splitext(file['name'])
            if file.get('subtype') and file['subtype'] is None:
                file.pop('subtype')

        return dict(
            name=self.granule,
            files=self.files
        )

    def get_json(self):
        """
        Returns the final CNM message dict, as json
        """
        output = json.dumps(self.message)
        return output
