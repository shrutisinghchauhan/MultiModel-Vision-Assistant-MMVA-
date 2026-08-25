# RAG-Based Offline Multi-Model Vision Chatbot with Decentralized Data

![first_screen](https://github.com/jot-s-bindra/Vision-Decentralized-Offline-Chatbot/assets/112833146/a2a65527-dfcc-4a6a-a037-8e7f75d48291)
![inference](https://github.com/jot-s-bindra/Vision-Decentralized-Offline-Chatbot/assets/112833146/20866aa0-2c67-4426-8f8c-8b6bcab0ed05)<!-- Add an image to represent your project -->

## Overview

This project hosts a fully offline multiModel -chatbot built on the Retrieval-Augmented Generation (RAG) model that even runs on CPU. It incorporates IPFS (pinata) technology for decentralized data storage, enabling secure and private interactions. The bot is designed to accept text prompts and images, utilizing a multimodal architecture to enhance language understanding.

Main feature is we havent used vision LLM but used multiple models which have allowed us to do this image task with text llm too,Multimodel architecture is shown in the photo given below.

Used thresholding to guide and manage multiple Models

## Multi-Model Architecture
![chatbot](https://github.com/jot-s-bindra/Vision-Decentralized-Offline-Chatbot/assets/112833146/19271f00-8d8a-437f-b967-9ebc02b83625)
## Features

- **Offline Chatbot**: Utilizes the RAG architecture for conversational AI.
- **Blockchain Data Storage**: Ensures decentralized and secure data handling.
- **Vision Integration**: Accepts images as prompts for interactions.Used MultiModel approach to include images as well in the prompt
- **Fine-Tuning**: Its easier to fine tune as you can fine tune or apply the vgg model only for your suitable task which is a lot easier and computationally inexpensive than fine tuning LLM.
- **Parameters**: Despite Using Multiple Models,Parameters are still lowers 7.6B model comprising all parameters of all the models .
- **Streamlit Hosted**: The bot is deployed using Streamlit for easy access.

## Architecture

The chatbot employs a multimodal architecture, harnessing the capabilities of various models:
- **LLama2-7b-chat-ggml**: Enhances language understanding.
- **VGG16 Fine-tuned on RAG Data**: Enables vision-based interactions.
- **Salesforce/blip-image-captioning-large**: Facilitates image captioning.
- **CLIP-ViT-L-14**: Encoder to map both image and text to same vector space.


## Setup

### Clone Repository and Install Dependencies

1. Clone the repository:

    ```bash
    git clone https://github.com/Purav001/Vision-Decentralized-Offline-Chatbot.git
    cd Vision-Decentralized-Offline-Chatbot
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
  ### Pull Docker Image

  Alternatively, you can pull the Docker image from [jasleenxddd/offlinemultimodelvisionchatbot](https://hub.docker.com/r/jasleenxddd/offlinemultimodelvisionchatbot):

```bash
docker pull jasleenxddd/offlinemultimodelvisionchatbot
```

### Download Required Models

1. Download the `llama2-7b-chat-ggml` model.[Download llama-2-7b-chat.ggmlv3.q8_0.bin](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q8_0.bin)

2. Run the `VGGTransferLearning.ipynb` notebook to generate `vgg16.h5`.

3. Place both the `llama2-7b-chat-ggml` model and `vgg16.h5` inside a folder named `models` in the root directory of the project.

### Run the Streamlit App

After downloading the necessary models:

```bash
streamlit run app.py
```
## Decentralizing file for chatbot training

You need to install the IPFS software on your machine. Here's how you can do it:

Step 1: Install IPFS

You can install IPFS using various methods depending on your operating system.

For instance, on Ubuntu, you can install IPFS using the package manager:

```sudo apt-get install curl
curl -sSL https://dist.ipfs.io/go-ipfs/v0.10.0/go-ipfs_v0.10.0_linux-amd64.tar.gz | sudo tar -xz -C /usr/local/bin ipfs
```
On macOS, you can use Homebrew:

```brew install ipfs```
For Windows, you can download the prebuilt binaries from the IPFS distributions .

Step 2: Initialize IPFS

Once IPFS is installed, you need to initialize it. This creates a new IPFS repository in your home directory:

```ipfs init```
Step 3: Start the IPFS Daemon

Now you can start the IPFS daemon:

```ipfs daemon```
This starts the IPFS daemon, which is a background process that handles adding and retrieving files from the IPFS network 1.

Note: The IPFS daemon must be running in order to add files to IPFS or retrieve files from it. If you stop the daemon, you'll need to restart it before you can perform these actions again.

 after the following run in new terminal 
 ```ipfs pin add FILE```
 the FILE that you want to add should be saved in the home directory
 
 after the following command you would get a CID or if you already have a CID 
 
 then you have to update the  `data` folder's file j.bat in windows :
 in your file  ```ipfs get <CID> ```
 
 then in cli get to the data folder in current directory  ```.\commands.bat```
 
 you have retrieved the required file successfully through the ipfs distributed p2p network.
 
 or else we can use pinning services like pinata here to pin our files.
 note:- in order to get your data decentralised you must copy the new.pdf file in your home directory and delete the file in data folder 
 ## IPFS WORKING 
![ipfs_chunker_4](https://github.com/jot-s-bindra/Vision-Decentralized-Offline-Chatbot/assets/112833146/17b099dd-e63d-4665-b998-4ba9e31c7001)
visual representation of how IPFS (InterPlanetary File System) handles chunking and deduplication of data. Here's a breakdown of the components shown in the image:

1. **Data Blocks**: These represent individual pieces of data that are broken down into smaller chunks. Each chunk is assigned a unique identifier or hash, which is used to reference it later.

2. **Chunking**: This is the process of breaking down data into smaller pieces, or chunks. In the context of IPFS, data is divided into fixed-size blocks, each of which is hashed and added to the IPFS network.

3. **Deduplication**: This is a process where IPFS checks if a piece of data already exists in the network before adding it. If a data block with the same hash already exists, IPFS reuses it instead of creating a new copy. This helps to save storage space and reduce redundancy.

4. **Block Exchange Protocol (BEP)**: This is a protocol used by IPFS for exchanging data blocks between nodes. When a node requests a data block, it contacts other nodes that have the block and negotiates a deal to exchange the block.

5. **Pinning**: Pinning is the process of telling an IPFS node to keep a certain file or data block around indefinitely. This ensures that the data remains available even if other nodes in the network go offline.

Overall, this image illustrates the core principles of how IPFS works: chunking data into blocks, deduplicating data to save storage space, and using a peer-to-peer network to exchange data blocks efficiently 
## Contributing

Contributions are welcome! If you want to contribute to this project, follow these steps:
1. Fork this repository.
2. Create a new branch (`git checkout -b feature/improvement`).
3. Make modifications and commit changes (`git commit -am 'Add feature/improvement'`).
4. Push the changes to your branch (`git push origin feature/improvement`).
5. Create a pull request.

