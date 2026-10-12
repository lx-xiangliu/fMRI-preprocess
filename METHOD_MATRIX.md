# Method comparison matrix

This matrix records the default starting point, credible alternatives, and the decision constraint for each survey subcategory. It is a guide for Code Agents; it does not claim one method is universally optimal.

| Subcategory | Default reference implementation | Alternatives to compare | Decision constraint |
|---|---|---|---|
| 1.1 Brain Shape | BIDS/NiBabel header comparison | fMRIPrep spatial normalization; ANTs/FSL resampling | Use explicit target grid; never pad silently |
| 1.2 Brain Orientation | NiBabel `as_closest_canonical` | fMRIPrep/FreeSurfer orientation handling | Preserve affine and verify axis codes |
| 1.3 Voxel Spacing | Header inspection + explicit resampling | ANTs/FSL `flirt` or Nilearn resampling | Choose grid from reference cohort |
| 1.4 Spatial Resolution | FOV/resolution report | ANTs/FSL/FreeSurfer registration | Do not infer resolution from shape alone |
| 1.5 Spatial Coordinates | Affine comparison | BIDS qform/sform + registration tools | Check world-coordinate tolerance |
| 2.1 TR | BIDS JSON `RepetitionTime` validation | fMRIPrep metadata propagation | Units are seconds; fail on missing metadata |
| 2.2 Sampling Rate | Explicit 1-D interpolation | Nilearn/AFNI temporal resampling | Only resample after deciding target TR |
| 2.3 Time Points | Explicit trim/pad policy | Censoring or learned masking | Padding is last resort and must be labeled |
| 2.4 Scan Duration | n_volumes × TR | BIDS validation and study-specific minimum | Use task design and power, not arbitrary cutoff |
| 3.1 Head Motion / FD | Power FD implementation | fMRIPrep confounds; ICA-AROMA | Use radius and motion convention consistently |
| 3.2 DVARS | Differenced RMS + robust flag | MRIQC/fMRIPrep DVARS | Inspect spikes jointly with motion |
| 3.3 Nonsteady State | Robust initial-volume detector | fMRIPrep nonsteady-state columns | Do not remove volumes without recording count |
| 3.4 Raw/Residual Artifacts | Robust MAD outlier mask | MRIQC, ICA-AROMA, tedana | Separate raw artifacts from residual QC |
| 3.5 Coverage / tSNR | Nonzero coverage + tSNR summary | MRIQC and fMRIPrep reports | Mask background before tSNR |
| 3.6 Registration Failure | Affine finiteness/determinant/overlap checks | ANTs/FSL registration QC | Review overlays for final acceptance |
| 3.7 Physiological Noise | RETROICOR-style sinusoidal regressors | PhysIO, aCompCor, tedana | Require recorded cardiac/respiratory traces |
| 3.8 Scanner Drift | Global-signal polynomial trend | fMRIPrep confounds; high-pass filtering | Do not remove neural low frequencies blindly |
| 3.9 WM/CSF Confounds | Explicit mask summary | aCompCor in fMRIPrep | Masks must be in same grid |
| 3.10 Other Non-neural | PCA variance summary | ICA-AROMA/tedana | Classify components before regression |
| 4.1 Mean | Robust global mean | Nilearn signal cleaning | Preserve units and scaling metadata |
| 4.2 Variance | Global/voxel variance | Standardization in Nilearn/fMRIPrep | Estimate after masking |
| 4.3 Signal Amplitude | Percent signal change | Nilearn standardization; task GLM scaling | Handle zero baseline explicitly |
| 4.4 Dynamic Range | 2nd–98th percentile range | MRIQC robust intensity metrics | Use robust percentiles rather than min/max |

Evidence labels: the small `src/` functions are tested locally; external tools are cited for comparison and are not silently run by this repository.
