import math

def gen_heart(radius: int, text: str):
    
    # radius - The radius of the circles inside the heart,
    #   this is roughly a third of the heart's height,
    #   or a quarter of the heart's width
    
    # text - The text with which the heart is filled
    
    # Starting triangle reduction value
    # Increase to make the bottom of the heart smaller
    # Default is 0
    reduction = 0
    
    # The value with which to increment the reduction
    # Increase this to round out the bottom of the heart
    # Default is 4
    reductionIncrement = 4
    
    # The reduction modifying function
    # Change this function to change the curvature of the bottom of the heart
    # Default is round(reduct ** 0.9975)
    def reductionFunction(reduct: int):
        return round(reduct ** 0.9975)
    
    characterIndex = 0  # Used later to iterate through the text
    circleMatrixLeft = []  # Matrix that defines the circle's shape
    
    def increment_char_index():
        nonlocal characterIndex
        characterIndex += 1
        if characterIndex >= len(text):
            characterIndex = 0
    
    # Circle generator
    
    # Turn the list into a matrix as tall as the diameter, +1 for the center
    for i in range(2 * radius + 1):
        circleMatrixLeft.append([])
    
        # Calculate the sine of every point inside the matrix
        # The matrix acts as a sort of unit circle
        #   with the middle corresponding to 0 and the edges to 1
        sine = 1 - abs((radius - i)/radius)
        
        # The sines of a circle with radius 2 can be put in the matrix like this:
        # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        # [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        # [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
        # The matrix is twice as long as it is tall
        #   because text in many monospace fonts is roughly twice as tall
        #   as it is wide
        # +1 to put one character as the central point
        for j in range(4 * radius + 1):
            # Calculate the relative cosine for every point in a list in the matrix
            #   similarly to the sine
            cosine = abs((2*radius - j)/(2*radius))
            
            # The cosines of a circle with radius 2 can be put in the matrix like this:
            # [1.0, 0.75, 0.5, 0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
            # [1.0, 0.75, 0.5, 0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
            # [1.0, 0.75, 0.5, 0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
            # [1.0, 0.75, 0.5, 0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
            # [1.0, 0.75, 0.5, 0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
            
            # Get the true sine from the cosine
            # The true sines of a circle with radius 2 can be put in the matrix like this:
            # [0.0, 0.66, 0.87, 0.97, 1.0, 0.97, 0.87, 0.66, 0.0]
            # [0.0, 0.66, 0.87, 0.97, 1.0, 0.97, 0.87, 0.66, 0.0]
            # [0.0, 0.66, 0.87, 0.97, 1.0, 0.97, 0.87, 0.66, 0.0]
            # [0.0, 0.66, 0.87, 0.97, 1.0, 0.97, 0.87, 0.66, 0.0]
            # [0.0, 0.66, 0.87, 0.97, 1.0, 0.97, 0.87, 0.66, 0.0]
            
            # When we add the true sines to the sines we defined before,
            #   the points inside the circle are greater or equal to 1
            #   and those outside the circle are smaller than 1
            
            # [0.0, 0.66, 0.87, 0.97, 1.0, 0.97, 0.87, 0.66, 0.0]
            # [0.5, 1.16, 1.37, 1.47, 1.5, 1.47, 1.37, 1.16, 0.5]
            # [1.0, 1.66, 1.87, 1.97, 2.0, 1.97, 1.87, 1.66, 1.0]
            # [0.5, 1.16, 1.37, 1.47, 1.5, 1.47, 1.37, 1.16, 0.5]
            # [0.0, 0.66, 0.87, 0.97, 1.0, 0.97, 0.87, 0.66, 0.0]

            if math.sin(math.acos(cosine)) + sine >= 1:
                # Add a character in every spot inside the circle
                # The symbol doesn't matter, it will get replaced with text later
                #   as long as it's not whitespace
                circleMatrixLeft[i].append("#")
            else:
                circleMatrixLeft[i].append(" ")  # Fill the rest with whitespace
    
    # Create a copy of the circle, removing the first column
    # This is because said column creates a gap between the circles at bigger sizes
    circleMatrixRight = [row[1:] for row in circleMatrixLeft]
    
    # Remove the last column of the circle
    # For smaller heart sizes, the extra distance makes the circles more defined,
    #   therefore only bigger sized hearts should have it removed
    if radius > 4:
        circleMatrixLeft = [row[:-2] for row in circleMatrixLeft]
    
    # Fill in the bottom right corner of the left circle
    for i in range(len(circleMatrixLeft)):
        if i > radius:
            for j in range(len(circleMatrixLeft[i])):
                # Decide the width of the corner based on
                #   f(x) = floor((1 + x/(10 + x/2)) + x^0925)
                if j > math.trunc((1 + radius/(10 + radius/(2))) * radius**0.925):
                    circleMatrixLeft[i][j] = "#"

    # Fill in the bottom left corner of the right circle
    for i in range(len(circleMatrixRight)):
        if i > radius:
            for j in range(len(circleMatrixRight[i])):
                # Since this time we're expanding the corner to the right,
                #   subtract the width from the total width of the circle
                #   taking into account the center
                if j < (4*radius - 1) - math.trunc((1 + radius/(10 + radius/(2))) * radius**0.925):
                    circleMatrixRight[i][j] = text[characterIndex]
                    
    # Concatenate the left and right circle
    for i in range(len(circleMatrixLeft)):
        circleMatrixLeft[i] += circleMatrixRight[i]
        
    # Replace every non-whitespace character with the text
    for i in range(len(circleMatrixLeft)):
        for char in range(len(circleMatrixLeft[i])):
            # Iterate and loop through the text, replacing each character in the matrix
            if circleMatrixLeft[i][char] != " ":
                circleMatrixLeft[i][char] = text[characterIndex]
                increment_char_index()
    
    # Triangle generator
    
    triangle = []  # Triangle matrix
    
    # Maximum triangle height is one radius
    # If it stops generating characters, it will cut off before it reaches the max
    for i in range(radius):
        triangle.append([])
        
        # Triangle gets offset by one character for bigger hearts
        # This is because of the added distance between circles for smaller triangles
        triangleShift = 1 if radius > 4 else 0
        
        # Add whitespaces according to radius and reduction
        for j in range(2 * radius + reduction - triangleShift):
            triangle[i].append(" ")
        # Add double as many characters, +1 for the center
        for j in range(radius * 4 - 2 * reduction + 1):
            triangle[i].append(text[characterIndex])
            increment_char_index()
            
        # Once no more characters are generated, stop generating
        if all(char == " " for char in triangle[i]):
            triangle.pop(i)
            break

        reduction += reductionIncrement
        reduction = reductionFunction(reduction)

    # Join the matrices into one string
    output = "\n"
    for line in circleMatrixLeft:
        output += "".join(line).rstrip()
        output += "\n"
    for line in triangle:
        output += "".join(line).rstrip()
        output += "\n"
        
    return output
        
if __name__ == "__main__":
    while True:
        try:
            size = int(input("Heart size: "))
            text = input("Filling text: ")
            print(gen_heart(size, text))
        except ValueError:
            print("Input size not a number!")
