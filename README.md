# NASA_LOST_DATA
NASA SPACE APPS CHALLANGE '19




THE CHALLANGE

Help find ways to improve the performance of machine learning and predictive models by filling in gaps in the datasets prior to model training.

ANATOMY OF THE CHALLANGE:

DO WHAT?

Improve performance of Machine Learning (ML) models by collecting a complete and continuous sensor data stream.

WHY DID IT HAPPEN?

    Sensor issues or signal noise due to experimental environment/setup
    Corrupted of data
    Loss of data during transmission (also due to limited bandwidth of transmission)
    Interference
    Limited amount of power for data collection and transmission

WHAT IT DOES?

    Limits the ability to train accurate ML models to predict features/characteristics in data, which in turn renders the data "useless"
    Hinders the collection of good-quality data silos

HOW TO SOLVE/OBJECTIVE?

    By "filling in" the missing datapoints in the datasets
    By "generating" the missing datapoints in the datasets
    By eliminating/removing the noisy/corrupted information that is embedded in individual datapoints

DO IT WHEN?

    Prior to training, i.e. during data cleaning and preprocessing.

We started by investigating the reasons behind data loss when the data is acquired through a sensor or sensor array. In addition, we also started doing research finding the reasons behind the loss.

Our research concluded that data loss in any dataset does not only occur due to missing data (be it discreet or continuous/timeseries) but also due to incomplete or corrupted or noisy collection of these data that are acquired by the sensors due to the reasons mentioned above.

HYPOTHESIS:

We propose an end-to-end Machine learning pipeline to -fill in the missing data using Generative modeling which involves using a model to generate new examples that plausibly come from an existing distribution of samples.

Stacked Denoising Autoencoder for when the sensor data is corrupted or there is a bit of noise in it, we call this type of data noisy data. To obtain proper information about the data, we want Denoising. We define our autoencoder to remove (if not all)most of the noise our data.

Transforms the input into a lower dimensional representation, and a decoder, which tries to reconstruct the original input from the lower dimensional representation. Therefore, these models present some some sort of “bottle neck” in the middle that forces the network to learn how to compress the data in a lower dimensional space. When training these algorithms, the objective is to be able to reconstruct the original input with the minimum amount of information loss. Once the model is trained, we can compress data at will by only using the encoder component of the autoencoder.

(A)

DETAILS: One model is called the “generator” or “generative network” model that learns to generate new plausible samples. The other model is called the “discriminator” or “discriminative network” and learns to differentiate generated examples from real examples.

The two models are set up in a contest or a game (in a game theory sense) where the generator model seeks to fool the discriminator model, and the discriminator is provided with both examples of real and generated samples.

After training, the generative model can then be used to create new plausible samples on demand.

(B)

An autoencoder is a neural network used for dimensionality reduction; that is, for feature selection and extraction. Autoencoders with more hidden layers than inputs run the risk of learning the identity function – where the output simply equals the input – thereby becoming useless.

Denoising autoencoders are an extension of the basic autoencoder, and represent a stochastic version of it. Denoising autoencoders attempt to address identity-function risk by randomly corrupting input (i.e. introducing noise) that the autoencoder must then reconstruct, or denoise.

Stacked Denoising Autoencoder

A stacked denoising autoencoder is simply many denoising autoencoders strung together.

A key function of SDAs, and deep learning more generally, is unsupervised pre-training, layer by layer, as input is fed through. Once each layer is pre-trained to conduct feature selection and extraction on the input from the preceding layer, a second stage of supervised fine-tuning can follow.

A word on stochastic corruption in SDAs: Denoising autoencoders shuffle data around and learn about that data by attempting to reconstruct it. The act of shuffling is the noise, and the job of the network is to recognize the features within the noise that will allow it to classify the input. When a network is being trained, it generates a model, and measures the distance between that model and the benchmark through a loss function. Its attempts to minimize the loss function involve resampling the shuffled inputs and re-reconstructing the data, until it finds those inputs which bring its model closest to what it has been told is true.

(C)

Encoder network: It translates the original high-dimension input into the latent low-dimensional code. The input size is larger than the output size. Decoder network: The decoder network recovers the data from the code, likely with larger and larger output layers.

The encoder network essentially accomplishes the dimensionality reduction, just like how we would use Principal Component Analysis (PCA) or Matrix Factorization (MF) for. In addition, the autoencoder is explicitly optimized for the data reconstruction from the code.

(D)

Disentangled Variational autoencoders

The idea of Variational Autoencoder is actually less similar to all the autoencoder models above, but deeply rooted in the methods of variational bayesian and graphical model. Instead of mapping the input into a fixed vector, we want to map it into a distribution. If each variable in the inferred latent representation is only sensitive to one single generative factor and relatively invariant to other factors, we will say this representation is disentangled or factorized. One benefit that often comes with disentangled representation is good interpretability and easy generalization to a variety of tasks.

For example, a model trained on photos of human faces might capture the gentle, skin color, hair color, hair length, emotion, whether wearing a pair of glasses and many other relatively independent factors in separate dimensions. Such a disentangled representation is very beneficial to facial image generation.

https://lilianweng.github.io/lil-log/2018/08/12/from-autoencoder-to-beta-vae.html#beta-vae
