# Image Sorter

Sorts images based on faces in the image. The application requires the user to add a picture of each face that is going to be used to sort the images, along with the name of the person.

When more than one "Known Face" is identified in a picture, it is moved to a folder with the name of each identified person.

If a "Known Face" is not identified in an image, the image will be placed in an "unknown" folder.

To run, install the required dependencies from the `requirements.txt` file. Then, run `python main.py`.

The `test` directory contains pictures to be sorted. When asked for "Known Faces," choose an image from the `known` directory and type a name into the input and click the "Add Image" button. Add the second face in the same manner. Click the "Next" button at the "Choose Known Faces" window, and then select the `unsorted` directory and click the "Next" button. Choose an output directory at the next window, and begin sorting.
