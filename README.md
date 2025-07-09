# AI-Powered Hearing Aid Using Deep Learning
AI-powered hearing aid for real-time noise reduction and speech enhancement.

This repository is a collection of software designed for a hearing aid system that leverages deep learning for **real-time speech de-noising**. The system is intended to run on an **NVIDIA Jetson Nano 2GB** and interfaces with an earpiece via the standard headphone and microphone jacks.

---

##  Objective

Enable a low-latency, real-time audio enhancement pipeline that removes background noise from speech using a Fully Convolutional Neural Network (FCNN).

---

##  Hardware Platform

- Jetson Nano 2GB
- Microphone and Headphone jacks
- External or onboard microphone

---

##  Processing Pipeline

The system processes audio in the following stages:

1. Short-Time Fourier Transform (STFT)
2. Fully Convolutional Neural Network (FCNN)
3. Inverse Short-Time Fourier Transform (ISTFT)

###  Model Details
- Sampling Rate: 22.05 kHz
- Input Window: 16 × 1024 samples = 0.743s
- Output Block: 1024 samples = 0.046s
- Target Latency: < 0.046 seconds
- Actual Latency on Jetson Nano: < 0.03 seconds
- Based on:
  - [Deep Learning for Audio Denoising (arXiv)](https://arxiv.org/pdf/1609.07132.pdf)
  - [Practical Deep Learning Audio Denoising Guide](https://sthalles.github.io/practical-deep-learning-audio-denoising/)

###  FCNN Architecture Features
- Skip connections for enhanced learning
- Kernel width = 1 for temporal compression
- Fully convolutional structure suitable for streaming input
