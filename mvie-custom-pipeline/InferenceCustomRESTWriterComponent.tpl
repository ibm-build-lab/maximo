[[define "inferencecustomrestwriter"]]    {
      "type": "MVIRESTWriter",
      "config": {
        "inputs": [
          "[[if .FilteredObjects]]filteredObjects[[else]]detectedObjects[[end]]"
        ],
        "outputs": [
          "imageData"
        ],
        "properties": {
          "bodyType": "multipart",
          "frameFormParam": "files",
          "individualPosts": false,
          "formParamTemplates": {
            "labels":"{\"labels\":[{{range $i,$obj := .[[if .FilteredObjects]]filteredObjects[[else]]detectedObjects[[end]]}}{{if gt $i 0}},{{end}}{\"name\":\"{{$obj.Label.Name}}\",\"confidence\":{{$obj.Score}},\"generate_type\":\"inferred\",\"bndbox\":{\"xmin\":{{$obj.Rectangle.Min.X}},\"ymin\":{{$obj.Rectangle.Min.Y}},\"xmax\":{{$obj.Rectangle.Max.X}},\"ymax\":{{$obj.Rectangle.Max.Y}}}{{$plen := len $obj.Polygons}}{{if gt $plen 0}},\"segment_polygons\":[{{range $k, $poly := $obj.Polygons}}{{if gt $k 0}},{{end}}[{{range $l, $vertice := $poly}}{{if gt $l 0}},{{end}}[{{index $vertice 0}},{{index $vertice 1}}]{{end}}]{{end}}]{{end}}}{{end}}]}",
            "user-metadata":"{\"station\":\"{{.context.Metadata.Station}}\",\"inspection\":\"{{.context.Metadata.Inspection}}\",\"device\":\"{{.context.Metadata.Device}}\",\"modelVersion\":\"{{.context.Metadata.MVIVersion}}\",\"modelUUID\":\"{{.context.Metadata.ModelUUID}}\",\"mxMonitoring\":\"{{.context.Metadata.MXMonitoring}}\"}"
          },
          "url": "https://a81f-129-41-59-7.ngrok-free.app/monitor/submit",
          "headers": {
              "X-Auth-Token": "test"
          },
          "requestQueueSenderPoolSize": 50
        }
      }
    }[[end]]
