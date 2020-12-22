# sitophila_spore_killer
Scripts used in "An introgressed gene causes meiotic drive in Neurospora sitophila" by Svedberg et al.

Reference: https://www.biorxiv.org/content/10.1101/2020.01.29.923946v1

## variantTab2fasta.py

This script will convert a GATK VariantsToTable file to an aligned fasta.

Usage:

```
variantTab2fasta.py --help
usage: variantTab2fasta.py [-h] [-g GENOME] [-n] [-c CONTIGS] [-r REFERENCE]
                            [-o OUTPUT] [-s SPLITTER]
                            filename

Script that converts a GATK VariantsToTable file to an aligned fasta.

positional arguments:
  filename              Variant table file name

optional arguments:
  -h, --help            show this help message and exit
  -g GENOME, --genome GENOME
                        Genome fasta file.
  -n, --nomissing       Outputs sites missing in the VCF file as dashes (-).
  -c CONTIGS, --contigs CONTIGS
                        List of contigs to export in quotations.
  -r REFERENCE, --reference REFERENCE
                        Includew reference genome. Reference strain name as
                        parameter.
  -o OUTPUT, --output OUTPUT
                        Output file name.
  -s SPLITTER, --splitter SPLITTER
                        Character that splits out strain name. Default=.
```



## fisherVCFcounts.py

This script performs Fisher's exact test on each site in order to perform a genome wide association test. You need three VCF files with genome wide SNP data of all samples, group 1 and group 2. If you have a single VCF file at the start, the workflow is as follows:

Create an allele counts file from the original VCF file. Then create text files containing the names of all individuals that belong to each group and use thes files to create allele counts files with only these individuals.

```
vcftools --vcf all_individuals.vcf --counts --out all_individuals
vcftools --vcf all_individuals.vcf --counts --keep group1.txt --out only_group1
vcftools --vcf all_individuals.vcf --counts --keep group2.txt --out only_group2
```

Then merge all three VCF files column wise using paste:

```
paste all_individuals.frq.counts only_group1.frq.count only_group2.frq.count > all.counts
```

Then extract biallelic sites:

```
awk '$3 == 2' all.counts > all.counts.biallelic
```

Then use `fisherVCFcounts.py` to perform Fisher's exact test on each site.

```
fisherVCFcounts.py all.counts.biallelic > all.counts.biallelic.fisher
```

You can also sort this file based on p-value to easily find outliers:

```
sort -k25g all.counts.biallelic.fisher > all.counts.biallelic.fisher.sorted
```
