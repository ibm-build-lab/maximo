[[$config := makeConfigMap . -]]
{
  "name": "[[.InspectionUUID]]",
  [[template "inferencevariables" $config]],
  [[template "metadata" $config]],
  "components": [
    [[template "imagereader" $config]],
    [[template "objectdetector" $config]],
    [[template "objectcropper" $config]],
    [[template "croppedimagewriter" $config]],
    [[template "inferencewriter" $config]]
  ]
}