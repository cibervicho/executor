# ascii_art.c: Generate Random ASCII Art Images

This program, `ascii_art.c`, written in C, creates a random image using ASCII art characters. It generates a grid of characters and assigns random symbols from a predefined set to each position, resulting in a visually interesting and unique image every time you run the program. 

## **What is ASCII Art?**

ASCII art is a type of image created using plain text characters, typically letters, numbers, and punctuation marks. By strategically arranging these characters, artists can create a surprising variety of shapes, patterns, and even representations of real-world objects.

## **How it Works:**

1. **Setting Up:**
    * The program defines constants `WIDTH` and `HEIGHT` to specify the dimensions of the generated image.
    * It declares an array of characters called `symbols` containing the set of symbols that will be used to build the image.
2. **Generating Randomness:**
    * The `srand(time(NULL))` function seeds the random number generator using the current system time as a starting point. This ensures that the generated image will be different each time you run the program.
3. **Creating the Image:**
    * The `generate_image` function takes a 2D character array (`image`) as input.
    * It iterates through each row (`y`) and column (`x`) of the `image` array.
    * For each position, it generates a random index within the `symbols` array. This index is used to select a random symbol from the set.
    * The chosen symbol is then assigned to the corresponding position in the `image` array.
4. **Printing the Image:**
    * The `main` function calls the `generate_image` function to create the random image.
    * It then iterates through the `image` array again, this time to print it to the console.
    * For each row, it prints all the characters in that row, followed by a newline character (`\n`) to move to the next line. This effectively prints the image row by row, creating the visual representation.

## **Building and Running the Program:**

1. **Prerequisites:**
    * You need a C compiler like GCC installed on your system.
2. **Compiling:**
    * Open a terminal or command prompt and navigate to the directory where you saved `ascii_art.c`.
    * Run the following command to compile the program:

    ```bash
    gcc ascii_art.c -o ascii_art  # Replace 'ascii_art' with your desired output filename (optional)
    ```

    This creates an executable file named `ascii_art` (or the name you specified) that you can use to run the program.
3. **Running:**
    * In the terminal, execute the program by typing:

    ```bash
    ./ascii_art
    ```

    This will generate a random ASCII art image and print it to the console.

## **Customization:**

* You can modify the `symbols` array to change the set of characters used to create the image. Experiment with different characters to achieve different visual effects.
* Adjust the `WIDTH` and `HEIGHT` constants to control the size of the generated image.
