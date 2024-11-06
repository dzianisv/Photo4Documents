async function loadImageToCanvas(imageElement) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = imageElement.width;
  canvas.height = imageElement.height;
  ctx.drawImage(imageElement, 0, 0);
  return canvas;
}

/**
 * To remove the background from an image using JavaScript, you can use TensorFlow.js with a pre-trained model like DeepLab. 
 * Below is an example of how you might set up such a function.
 * @param {*} imageElement 
 * @returns 
 */

async function removeBackground(imageElement) {
  try {
    const inputCanvas = await loadImageToCanvas(imageElement);

    // Load the DeepLab model
    const model = await deeplab.load({ base: 'pascal', quantizationBytes: 4 });

    // Perform segmentation
    const { segmentationMap } = await model.segment(inputCanvas);

    // Create a canvas to draw the output
    const outputCanvas = document.createElement("canvas")
    const ctx = outputCanvas.getContext('2d');
    outputCanvas.width = inputCanvas.width;
    outputCanvas.height = inputCanvas.height;

    // Draw the original image
    ctx.drawImage(inputCanvas, 0, 0);

    // Get image data
    const imageData = ctx.getImageData(0, 0, outputCanvas.width, outputCanvas.height);
    const data = imageData.data;

    // Remove background by setting non-object pixels to transparent
    for (let i = 0; i < data.length; i += 4) {
      const segmentValue = segmentationMap[i / 4];
      if (segmentValue !== 15) { // 15 is the label for 'person' in PASCAL VOC
        data[i + 3] = 0; // Set alpha to 0
      }
    }

    // Put the modified image data back to the canvas
    ctx.putImageData(imageData, 0, 0);

    // Return the canvas as an image
    const outputImage = new Image();
    outputImage.src = outputCanvas.toDataURL();

    return outputImage;
  } catch (error) {
    console.error('Error removing background:', error);
    throw error;
  }
}