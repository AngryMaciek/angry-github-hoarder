# Angry GitHub Hoarder :hamster:

In the event of a global zombie apocalypse GitHub servers would most probably get shut down.  
It is not very wise to keep all the code on their servers **exclusively**.  
I have put together a small _Python_ script that creates a local copy of all my work.  

Ironically, I package it as a repo... and upload to GitHub -_-

### _conda_ env setup
```
conda create --name github-hoarder
conda activate github-hoarder
conda install pip
pip install PyGithub
```
