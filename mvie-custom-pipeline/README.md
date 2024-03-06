# Pipelines

Pipelines in Maximo Visual Inspection Edge is chain of components which is configured in JSON.

## 1. InferenceCollectionFolderCropped.tpl - Get Cropped image

   File [InferenceCollectionFolderCropped.tpl](InferenceCollectionFolderCropped.tpl) returns cropped image where object is detected and writes inference.

## 2. InferenceCustomRestWritter.tpl - Make REST API call to external system
   * This pipeline is created to send inference results to external system. It makes REST API call to send inference result.
   * Open [InferenceCustomRESTWriterComponent.tpl](InferenceCustomRESTWriterComponent.tpl) and update the `URL`, `headers` as per need. Upload InferenceCustomRESTWriterComponent.tpl file to <INSTALL_ROO>/vision-edge/volume/run/var/config/templates/components folder where Maximo Visual Inspection Edge is installed.
   * Navigate to MVI Edge and go to pipelines. Upload [InferenceCustomRestWritter.tpl](InferenceCustomRestWritter.tpl) file as a pipeline.
   * Use this pipeline in configuration of inspection.
  
   Use below python flask snipped to retrieve the inference result from MVI Edge.

   ~~~~
   @app.route("/monitor/submit", methods=['POST'])
   def mvi_inference():
      incoming_request = request.files['files']

      print('incoming_request, incoming_request')
      print(request.headers)

      label = request.form['labels']
      metadata = request.form['user-metadata']
      print('label', label)
      print('metadata', metadata)
      
      return "OK"
   ~~~~

   

   
