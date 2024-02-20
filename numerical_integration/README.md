# 2. &nbsp; Numerical integration methods
This project focuses on numerical integration methods for approximating the definite integral of a given function. It explores various numerical techniques, compares their convergence behavior, and evaluates their accuracy.

## File description
#### <a href="integration_methods_convergence.ipynb">`integration_methods_convergence.ipynb`</a>
The project is realized using a Jupyter notebook, which also goes into more detail about the inner workings of the programs.

## Dependencies
This project requires the following Python libraries:
`numpy`
`scipy`
`matplotlib`
`sklearn`

They can be installed using PIP:
```
pip install numpy scipy matplotlib scikit-learn
```

## Installation
Re-running the code in this notebook requires an installation of Python 3 and the libraries mentioned above. No external files are needed.

## Usage
The notebooks are annotated and self-explanatory. The implementation of the integration methods was realized using `numpy` and heavily relies on array slicing, leading highly efficient computation compared to more naive approaches.

## Graphical output
<img src="output/convergence_order.png" alt="Convergence order plot of different integration methods">

***Figure 2.1:** Resulting convergence order plot of the four tested integration methods.*

## Contributing
If you want to contribute to this project, found any bugs or have new feature ideas, please open an issue!

## License
This project is licensed under the **GNU General Public License v3.0**, allowing you to freely use, modify, and distribute the code. Any derived works must also be licensed under GPL-3.0, promoting open-source collaboration and transparency. Please review the license terms before using or contributing to this project.
