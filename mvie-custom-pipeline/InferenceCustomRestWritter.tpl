[[$config := makeConfigMap . -]]
{
  "name": "[[.InspectionUUID]]",
  [[template "inferencevariables" $config]],
  [[template "metadata" $config]],
  "components": [
    [[template "imagereader" $config]],
    [[template "objectdetector" $config]],
    [[template "fileimagewriter" $config]],
    [[template "inferencewriter" $config]],
    [[template "inferencecustomrestwriter" $config]]
  ]
}