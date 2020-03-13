import pydicom as dicom



dicom_names = ["IMG-0004-00001.dcm","IMG-0004-00002.dcm", "IMG-0004-00003.dcm", "IMG-0004-00004.dcm"]


for dcm in dicom_names:
  dicomfile = dicom.read_file(dcm)
  dicomfile.PhotometricInterpretation = "RGB"
  dicomfile.save_as(dcm)