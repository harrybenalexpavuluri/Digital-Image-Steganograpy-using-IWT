import cv2
import numpy as np
import matplotlib.pyplot as plt

stego_img = cv2.imread("stego.png", 0)
stego_flatten = stego_img.flatten()

out = []
for x in stego_flatten:
    # step 2: change pixel value to binary
    x = np.binary_repr(x, width=8)

    # step 3: perform XOR on 7th and 6th bits
    xor_a = int(x[1]) ^ int(x[2])
    
    # step 4: perform XOR operation on 8th bit with xor_a
    xor_b = int(x[0]) ^ xor_a
    
    # step 5: perform XOR operations on message bits with 3 MSB
    xor_c = int(x[-1]) ^ xor_b
    
    out.append(int(xor_c))

recover_img = np.reshape(np.array(out), (256,256))
recover_img[recover_img==1] = 255

cv2.imwrite('git.png',recover_img)

plt.title("Recovered Image")
plt.axis("off")
plt.imshow(recover_img, cmap="gray")
plt.show()
