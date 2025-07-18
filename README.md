# M-PACT: Mammography Pressure and Compression tracking for Quality Control

>:warning: **This is a preliminary version of the M-PACT software! (only for revision)**
> 
>Before continuing, please, check our paper "M-PACT: A mechanics based toolkit to evaluate 
breast compression in mammography and DBT" **(currently under review)**

## Overview

Breast compression plays a critical role in mammography and digital breast tomosynthesis (DBT),
improving image quality while reducing radiation dose and tissue superposition.
Unfortunately, many women experience pain and discomfort during the procedure, 
and current guidelines in mammography acquisition remain vague about how much compression should be applied.

In our paper, we analyse the mammographic compression from a physical and mechanical perspective. 
By modeling the mammography compression as a uniaxial compression problem, we applied continuum mechanics to determine
the physical equations governing the relationship between uncompressed and compressed breast states.

Based  on our findings, we developed **M-PACT**, a framework to assist radiologists, medical physicists, and researchers
in analyzing breast compression. Our software is capable of estimating a suitable thickness
range, and objectively evaluate the degree of compression of already acquired mammograms calculating a quantitative 
compression score, defined as the number of standard deviations the measured thickness deviates from the expected value.
This score enables to categorize the mammograms as *within the normal range* or potentially *undercompressed*, and 
*overcompressed*, offering a standardized and reproducible method to monitor and improve compression practices.

[comment]:<> (This tool has potential applications in quality control, technologist training, and even real-time clinical 
decision support, offering a standardized and reproducible method to monitor and improve compression practices.)

[comment]:<> (By bridging the gap between physical modeling and clinical practice, our work aims to support a more personalized 
and standardized compression approach)

The software offers two operating modes: prediction and evaluation.


## M-PACT - Prediction mode

In prediction mode, the user provides the patient breast volume (BV) and mammographic view as input, and the software
estimates the expected thicknes  by means of the equations derived from full-field digital mammograms, along with 
two standard deviations range obtained from the residual errors. 

Function ```main()``` provides a simple interface between the terminal and  ```MPACT()```. A simple query for a breast 
with volume of $1,000~cm^3$ under a *CC* compression is:

```commandline
> python main.py --BreastVolume 1000 --MammographyView CC
```

or, in a shortest way:

```commandline
> python main.py -BV 1000, -V CC
```

obtaining the following results:

```commandline
MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)

Arguments:
        Breast Volume (cm3): 1000
        Mammography projection: CC
        Sigma threshold: 2

Expected Thickness: 6.204 cm
Expected Thickness range: [5.1, 7.31] cm
```

As shown, the expected thickness range using two standard deviations varies between $5.1$ and $7.31~cm$

We have to point out that FFDM-derived measures were obtained using the commercial software Volpara$^{TM}$ (v.1.5.11), 
year 2013, which provides relevant metrics, such as total breast volume (cm3), contact area between the breast and 
compression paddle (cm2), compression pressure, (kPa), and a categorical density grade (VDG). However, this measures 
may not held consistent across different versions, softwares or other methodologies to calculate BV, such as water displacement, 
 Grossman disk, or 3D medical image modalities and depth cameras, as exposed in the paper.

Incorporating compression force enables a more complete analysis. According to our data, compression forces typically
fall between $50$ and $200~N$. The compressed breast thickness can also be obtained as a function of the ratio between 
breast volume and applied force as exposed in the paper.  

To incorporate the compression force into our analysis, we have to include options ```--CompressionForce'``` of ```-F```
into our query.

```commandline
> python main.py -BV 1000 -V CC -F 150
```

obtaining:

```commandline
MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)

Arguments:
        Breast Volume (cm3): 1000
        Mammography projection: CC
        Compression Force (N): 150
        Sigma threshold: 2

Expected Thickness: 6.237 cm
Expected Thickness range: [5.24, 7.23] cm
```

Note that values out of range in both BV and compression force may obtain weird results.

The expected thickness range can also be modified by changing the *sigma threshold*. Using $\sigma=2$ we are obtaining a 
two standard deviations thickness range calculated from the residual errors. However, if you are interested on using a
custom standard deviation range, it can be modified by including ```--Sigma``` or ```-S``` 
into your query. 

For instance, using three standard deviations, $\sigma=3$, we obtain:

```commandline
> python main.py -BV 1000 -V CC -F 150 -S 3


MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)

Arguments:
        Breast Volume (cm3): 1000
        Mammography projection: CC
        Compression Force (N): 150
        Sigma threshold: 3.0

Expected Thickness: 6.237 cm
Expected Thickness range: [4.74, 7.73] cm
```

## M-PACT - Evaluation mode

Our software also allows to evaluate already acquired mammograms. By including the compressed
breast thickness, ```--Thickness``` or ```-T```, the software calculates a quantitative compression score, $s$,
defined as the number of standard deviations the measured thickness deviates from the expected value. 
The expected thickness values is computed using the compression force, if available, or without this value, 
using just the BV value. In this way attending to the threshold of sigma, the compression can be categorized into 
*within normal range*, or potentially *undercompressed*, and *overcompressed*. 

For instance, using the query: 

```commandline
python main.py -BV 1000 -V CC -F 150 -T 6.5
```

obtaining:

```commandline
MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)

Arguments:
        Breast Volume (cm3): 1000
        Mammography projection: CC
        Compression Force (N): 150
        Recorded Breast Thickness (cm): 6.5
        Sigma threshold: 2


Expected Thickness: 6.237 cm
Expected Thickness range: [5.24, 7.23] cm

S-score value: 0.53
Within the normal range
```

Categorizing the compression within the normal range. However, changing the compressed thickness value from $T=6.5~cm$ 
to $T=7.5~cm$, we obtain.

```commandline
> python main.py -BV 1000 -V CC -F 150 -T 7.5


MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)

Arguments:
        Breast Volume (cm3): 1000
        Mammography projection: CC
        Compression Force (N): 150
        Recorded Breast Thickness (cm): 7.5
        Sigma threshold: 2
    
Expected Thickness: 6.237 cm
Expected Thickness range: [5.24, 7.23] cm

S-score value: 2.53
Recorded thickness is larger than the expected maximum: 7.5 > 7.23
Potentially overcompressed
```

To save our results, we have to include the patient ID o image name, using ```--PatientID``` or just ```-ID```, and the
output file path, ```--outputfile``` or ```-o```. The *.csv* file stores the information, including issues yielded during
the evaluation.

## Processing datasets and visualizing results

Since manually processing a large dataset may be annoying and time consuming, we provide a faster way using a *.csv* file.
The file have to contain at least columns named **PatientID**, **BreastVolumeCm3**, and **MammographyView** to computed
the expected thickness range, but **CompressionForceN** can also be included. However, sigma value needs to be manually
defined in the terminal prompt.

If the file contains a column named **ThicknessCm**, it directly uses the evaluation mode, computing the *s-score* value
and providing the corresponding classification.

When using ```--use_csv``` option, providing a output *.csv* file path is mandatory. The output filename has to be different
than the input one to avoid overwriting the document. 

```commandline
> python main.py --use_csv ~/M-PACT/test.csv --outputfile ~/M-PACT/output.csv
```

Furthermore, we included an option to visualize the processed data (just in the evaluation mode) into the expected 
distribution.  