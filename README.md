# National Monuments Public Comments Project
A text analytics project to discover insights in the FR-2017-09490 National Monuments Public Comments dataset.

## Environment
This project is created using freely available tools. These include:
* Python 3.6
* NumPy
* SciPy
* SciKit-Learn
* Jupyter Notebook
* [Lightside](http://www.cs.cmu.edu/~cprose/LightSIDE.html)


### Environment Setup
To create a virtual environment for this project using Anaconda (a virtual environment manager), run the commands below:
```bash
conda create -y -n comments python=3.6 jupyter numpy scipy scikit-learn
source activate comments
jupyter notebook
```

#### Git Large File Storage
Because the comments dataset (data/comments.csv) exceeds Git's maximum file size of 100mb, it is stored using Git Large File Storage. To commit changes, you may need Git Large File Storage installed. Follow the instructions at [Git LFS](https://git-lfs.github.com/) to install Git LFS, e.g.
```bash
brew install git-lfs
git lfs install
```