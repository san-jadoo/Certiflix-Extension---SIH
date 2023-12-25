# Certiflix Extension

This is the extension for image correctness for a product on a flipkart marketplace.
Steps involved here ..
1. Extension added to our chrome browser, which contains two buttons verify and close, Whenever the verify button clicked, Process starts
2. Scrap the product images and description from the flipkart websites.
3. Product image will send to the product identifier model which is deep neural network mobilenet model which identify the product
4. Then logo of that product is identified and check whether it is relevant to that product or any other fake product logo, yolo object detection is used here
5. Finally description is checked with the text extracted from the product images.
6. If any of the above failed, the product may be fake/irrevelant one.Otherwise product is verified successfully.
