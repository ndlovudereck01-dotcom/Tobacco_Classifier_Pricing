# Model Files Directory

This directory should contain the following machine learning model files:

1. `tobacco_detector.h5` - Model for detecting tobacco leaves in images
2. `2classifier_model.h5` - Model for classifying tobacco quality grades
3. `2label_binarizer.pkl` - Label binarizer for the classification model
4. `nn_pricing.h5` - Neural network model for predicting tobacco prices
5. `nn_encoder.npy` - Encoder for the pricing model

## How to add the models

1. Copy the model files to this directory
2. Make sure the file names match exactly as listed above
3. No modifications to the files should be needed

## Model details

### Tobacco Detector
- Detects if an image contains a tobacco leaf
- Uses MobileNetV2 architecture
- Input shape: (224, 224, 3)
- Output: Binary classification (tobacco/not tobacco)

### Classifier Model
- Classifies tobacco leaves into quality grades
- Uses MLP architecture
- Requires features extracted from color and texture analysis
- Output: Multi-class classification of tobacco grades

### Pricing Model
- Predicts tobacco price based on quality grade
- Uses neural network architecture
- Input: One-hot encoded tobacco grade
- Output: Estimated price in currency units
