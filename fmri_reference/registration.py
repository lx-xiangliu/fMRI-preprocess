"""Low-resolution teaching registration; never substitute for fMRIPrep validation."""
import numpy as np
import SimpleITK as sitk

def rigid(fixed_path,moving_path,output_path,metric='mi'):
    fixed=sitk.ReadImage(str(fixed_path),sitk.sitkFloat32)
    moving=sitk.ReadImage(str(moving_path),sitk.sitkFloat32)
    if fixed.GetDimension()!=3 or moving.GetDimension()!=3:raise ValueError('3D images required')
    tx=sitk.CenteredTransformInitializer(fixed,moving,sitk.Euler3DTransform(),sitk.CenteredTransformInitializerFilter.GEOMETRY)
    reg=sitk.ImageRegistrationMethod()
    if metric=='mi':reg.SetMetricAsMattesMutualInformation(32)
    elif metric=='correlation':reg.SetMetricAsCorrelation()
    else:raise ValueError('Unknown metric')
    reg.SetMetricSamplingStrategy(reg.RANDOM);reg.SetMetricSamplingPercentage(.2,seed=42)
    reg.SetInterpolator(sitk.sitkLinear)
    reg.SetOptimizerAsRegularStepGradientDescent(1.,.001,80)
    reg.SetOptimizerScalesFromPhysicalShift()
    reg.SetShrinkFactorsPerLevel([4,2,1]);reg.SetSmoothingSigmasPerLevel([2,1,0]);reg.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
    reg.SetInitialTransform(tx,inPlace=True)
    before=float(reg.MetricEvaluate(fixed,moving));reg.Execute(fixed,moving);after=float(reg.MetricEvaluate(fixed,moving))
    out=sitk.Resample(moving,fixed,tx,sitk.sitkLinear,0.,sitk.sitkFloat32);sitk.WriteImage(out,str(output_path))
    return {'metric':metric,'objective_before':before,'objective_after':after,'optimizer_stop':reg.GetOptimizerStopConditionDescription(),
            'parameters_euler_lps':list(tx.GetParameters()),'fixed_to_moving_lps':True,
            'clinical_registration_pass':'NOT_ASSESSED','seed':42}
