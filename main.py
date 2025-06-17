from tkinter import messagebox, simpledialog, filedialog
from tkinter import *
import tkinter.ttk as ttk  # For enhanced button styling
import cv2
import numpy as np
from keras.models import model_from_json, load_model
from matplotlib import pyplot as plt
from random import randrange
from numpy.random import randn
from PIL import Image, ImageTk  # Import for image resizing

def open_main():
    # Initialize main window

    main = Tk()
    main.title("A Hybrid CNN Model for Diabetic Retinopathy Classification")
    main.geometry("1500x1500")  # Increased screen size
    main.state('zoomed')  # Start in full-screen mode

    # Load and resize background image dynamically
    def update_bg():
        bg = Image.open('background3.png')  # Load image
        bg = bg.resize((main.winfo_width(), main.winfo_height()), Image.LANCZOS)  # Resize to window size
        bg_img = ImageTk.PhotoImage(bg)
        bg_label.config(image=bg_img)
        bg_label.image = bg_img

    # Create canvas for full-screen background
    bg_label = Label(main, bg='black', highlightthickness=5, highlightbackground='gray')
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Bind resizing event to update the background image
    main.bind("<Configure>", lambda e: update_bg())

    # Define button styles with 3D effects
    def on_enter(e):
        e.widget.config(bg='#D3D3D3', relief=GROOVE, fg='black')  # Red with black text when hovered

    def on_leave(e):
        e.widget.config(bg='#333333', relief=GROOVE, fg='white')  # Dark background and white text when not hovered

    # Button Factory for individual 3D-style buttons with reduced size and gap
    def create_button(text, command, y_pos):
        btn = Button(main, text=text, command=command, 
                    bg='#333333', fg='white', activebackground='#444444',
                    activeforeground='white', relief=GROOVE, 
                    font=('Helvetica', 12, 'bold'), width=30, height=2,
                    highlightthickness=2, highlightbackground='#555555', highlightcolor='#555555',
                    borderwidth=4)
        btn.place(x=50, y=y_pos)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # Upload dataset function
    def upload():
        global filename
        filename = filedialog.askdirectory(initialdir=".")
        text.delete('1.0', END)
        text.insert(END, filename + " loaded\n")

    # Generate latent points
    def generate_latent_points(latent_dim, n_samples):
        x_input = randn(latent_dim * n_samples)
        x_input = x_input.reshape(n_samples, latent_dim)
        return x_input

    # Create image plot
    def create_plot(examples, n):
        for i in range(n * n):
            plt.subplot(n, n, 1 + i)
            plt.axis('off')
            plt.imshow(examples[i, :, :])
        plt.show()

    # Load GAN model
    def ganModel():
        global gan_model, image_count
        gan_model = load_model('model/generator_model_080.h5')
        latent_points = generate_latent_points(200, 200)
        X = gan_model.predict(latent_points)
        image_count = X.shape[0]
        text.insert(END, 'GAN model loaded\n')
        text.insert(END, 'Total images generated: ' + str(image_count) + "\n")
        create_plot(X, 10)

    # Load prediction model
    def predictModel():
        global predict_model
        with open('model/train.json', "r") as json_file:
            predict_model = model_from_json(json_file.read())
        predict_model.load_weights("model/train.h5")
        text.insert(END, 'Prediction model loaded successfully\n')

    # Predict severity
    def getPrediction(img):
        img1 = np.asarray(img).reshape(1, 32, 32, 3)
        preds = predict_model.predict(img1)
        predict = np.argmax(preds)
        result_labels = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']
        return result_labels[predict]

    def predictSeverity():
        global image_count
        latent_points = generate_latent_points(200, 200)
        X = gan_model.predict(latent_points)
        image_count = X.shape[0]

        # Display messages before generating images
        text.insert(END, "GAN model loaded\n")
        text.insert(END, "Total images generated: " + str(image_count) + "\n")
        text.insert(END, "Prediction model loaded successfully\n")
        text.insert(END, "Total images generated: " + str(image_count) + "\n")
        
        # Initialize counters for each severity level
        normal_count = 0
        mild_count = 0
        moderate_count = 0
        severe_count = 0
        proliferative_count = 0
        
        predictions = []
        
        for i in range(20):  # Predict on 20 images first
            img = X[i, :, :]
            result = getPrediction(img)
            predictions.append((i, img, result))  # Store image and result
            
            # Update counters before displaying images
            if result == 'No DR':
                normal_count += 1
            elif result == 'Mild':
                mild_count += 1
            elif result == 'Moderate':
                moderate_count += 1
            elif result == 'Severe':
                severe_count += 1
            elif result == 'Proliferative DR':
                proliferative_count += 1

        # Display the counts before showing images
        text.insert(END, "Normal: " + str(normal_count) + "\n")
        text.insert(END, "Mild: " + str(mild_count) + "\n")
        text.insert(END, "Moderate: " + str(moderate_count) + "\n")
        text.insert(END, "Severe: " + str(severe_count) + "\n")
        text.insert(END, "Proliferative DR: " + str(proliferative_count) + "\n")

        # Force update of text area before proceeding
        text.update()

        # Now display the images with their predicted severity
        for i, img, result in predictions:
            img_resized = cv2.resize(img, (300, 300))
            cv2.putText(img_resized, 'Prediction: ' + result, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow('Image ID: ' + str(i) + ' Prediction: ' + result, img_resized)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Exit function
    def closeApp():
        main.destroy()

    # Title label
    title = Label(main, text='A Hybrid CNN Model for Diabetic Retinopathy Classification', bg='#D3D3D3', fg='black',
                font=('times', 20, 'bold'), padx=10, pady=20, width=48,relief=RAISED, bd=3,
                highlightthickness=3, highlightbackground='#888888')  # Adjusted width to fit properly
    title.place(relx=0.5, rely=0.05, anchor='center')  # Center horizontally

    # Output text area
    text = Text(main, height=18, width=65, font=('times', 12, 'bold'), highlightthickness=3, highlightbackground='black', bg='#D3D3D3',fg="black")
    text.place(x=700, y=180)                                                                                              # verydarkgrey

    # Create buttons with 3D style and added gap between buttons
    uploadButton = create_button("Upload Fundus Dataset", upload, 200)
    ganButton = create_button("Load GAN Model", ganModel, 270)
    modelButton = create_button("Load Prediction Model", predictModel, 340)
    predictButton = create_button("Generate GAN Image & Predict Severity", predictSeverity, 410)
    closeButton = create_button("Exit", closeApp, 480)

    # Hide buttons and text area initially
    uploadButton.place_forget()
    ganButton.place_forget()
    modelButton.place_forget()
    predictButton.place_forget()
    closeButton.place_forget()
    text.place_forget()

    # Show background image for 3 seconds
    main.after(3000, lambda: [uploadButton.place(x=100, y=200), ganButton.place(x=100, y=270),
                            modelButton.place(x=100, y=340), predictButton.place(x=100, y=410),
                            closeButton.place(x=100, y=480), text.place(x=700, y=180)])

    # Start the Tkinter main loop
    main.mainloop()
    import logging

    # Create a logger
    logger = logging.getLogger('diabetic_retinopathy_classification')
    logger.setLevel(logging.INFO)

    # Create a file handler and a stream handler
    file_handler = logging.FileHandler('diabetic_retinopathy_classification.log')
    stream_handler = logging.StreamHandler()

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Modify existing functions to include logging
    def upload():
        global filename
        filename = filedialog.askdirectory(initialdir=".")
        text.delete('1.0', END)
        text.insert(END, filename + " loaded\n")
        logger.info('Dataset uploaded successfully')

    def ganModel():
        global gan_model, image_count
        gan_model = load_model('model/generator_model_080.h5')
        latent_points = generate_latent_points(200, 200)
        X = gan_model.predict(latent_points)
        image_count = X.shape[0]
        text.insert(END, 'GAN model loaded\n')
        text.insert(END, 'Total images generated: ' + str(image_count) + "\n")
        create_plot(X, 10)
        logger.info('GAN model loaded successfully')

    def predictModel():
        global predict_model
        with open('model/train.json', "r") as json_file:
            predict_model = model_from_json(json_file.read())
        predict_model.load_weights("model/train.h5")
        text.insert(END, 'Prediction model loaded successfully\n')
        logger.info('Prediction model loaded successfully')

    def predictSeverity():
        global image_count
        latent_points = generate_latent_points(200, 200)
        X = gan_model.predict(latent_points)
        image_count = X.shape[0]

        # Display messages before generating images
        text.insert(END, "GAN model loaded\n")
        text.insert(END, "Total images generated: " + str(image_count) + "\n")
        text.insert(END, "Prediction model loaded successfully\n")
        text.insert(END, "Total images generated: " + str(image_count) + "\n")
        
        # Initialize counters for each severity level
        normal_count = 0
        mild_count = 0
        moderate_count = 0
        severe_count = 0
        proliferative_count = 0
        
        predictions = []
        
        for i in range(20):  # Predict on 20 images first
            img = X[i, :, :]
            result = getPrediction(img)
            predictions.append((i, img, result))  # Store image and result
            
            # Update counters before displaying images
            if result == 'No DR':
                normal_count += 1
            elif result == 'Mild':
                mild_count += 1
            elif result == 'Moderate':
                moderate_count += 1
            elif result == 'Severe':
                severe_count += 1
            elif result == 'Proliferative DR':
                proliferative_count += 1

        # Display the counts before showing images
        text.insert(END, "Normal: " + str(normal_count) + "\n")
        text.insert(END, "Mild: " + str(mild_count) + "\n")
        text.insert(END, "Moderate: " + str(moderate_count) + "\n")
        text.insert(END, "Severe: " + str(severe_count) + "\n")
        text.insert(END, "Proliferative DR: " + str(proliferative_count) + "\n")

        # Force update of text area before proceeding
        text.update()

        # Now display the images with their predicted severity
        for i, img, result in predictions:
            img_resized = cv2.resize(img, (300, 300))
            cv2.putText(img_resized, 'Prediction: ' + result, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow('Image ID: ' + str(i) + ' Prediction: ' + result, img_resized)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        logger.info('Severity prediction completed successfully')

    def closeApp():
        main.destroy()
        logger.info('Application closed') 
    
