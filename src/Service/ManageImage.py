import SimpleITK as sitk
import os
import config
from math import pi


class ManageImage:

    def __init__(self):
        return

    def readImage(self, filename):
        reader = sitk.ImageFileReader()
        reader.SetImageIO("TIFFImageIO")
        reader.SetFileName(filename)
        reader.SetOutputPixelType(sitk.sitkFloat32)
        image = reader.Execute()
        return image

    def saveImage(self, filename, image):

        sitk.WriteImage(image, filename, False)
        print('Saved image: ' + filename)
        return

    def saveTransform(self, registrationResult, filename):
        sitk.WriteTransform(registrationResult, filename)
        print('Saved transform: ' + filename)

    # lambda function to fix parameters
    def commandIteration(self, method):
        print("{0:3} = {1:10.5f} : {2}".format(method.GetOptimizerIteration(),
                                               method.GetMetricValue(),
                                               method.GetOptimizerPosition()))

    def registrationMethodTranslation(self, imageFixed, imageMoving):
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsMeanSquares()
        registration.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
        registration.SetInitialTransform(sitk.TranslationTransform(imageFixed.GetDimension()))
        registration.SetInterpolator(sitk.sitkLinear)
        registration.AddCommand(sitk.sitkIterationEvent, lambda: self.commandIteration(registration))

        out = registration.Execute(imageFixed, imageMoving)
        return out

    def registrationMethodTranslation2(self, imageFixed, imageMoving):
        imageFixed = sitk.Normalize(imageFixed)
        imageFixed = sitk.DiscreteGaussian(imageFixed, 2.0)
        imageMoving = sitk.Normalize(imageMoving)
        imageMoving = sitk.DiscreteGaussian(imageMoving, 2.0)
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsJointHistogramMutualInformation()
        registration.SetOptimizerAsGradientDescentLineSearch(learningRate=1.0,
                                                             numberOfIterations=200,
                                                             convergenceMinimumValue=1e-5,
                                                             convergenceWindowSize=5)
        registration.SetInitialTransform(sitk.TranslationTransform(imageFixed.GetDimension()))
        registration.SetInterpolator(sitk.sitkLinear)
        registration.AddCommand(sitk.sitkIterationEvent, lambda: self.commandIteration(registration))
        out = registration.Execute(imageFixed, imageMoving)
        return out

    def registrationMethodCenteredTransform(self, imageFixed, imageMoving):
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsCorrelation()
        registration.SetOptimizerAsRegularStepGradientDescent(learningRate=2.0,
                                                              minStep=1e-4,
                                                              numberOfIterations=500,
                                                              gradientMagnitudeTolerance=1e-8)
        registration.SetOptimizerScalesFromIndexShift()
        tx = sitk.CenteredTransformInitializer(imageFixed, imageMoving, sitk.Similarity2DTransform())
        registration.SetInitialTransform(tx)
        registration.SetInterpolator(sitk.sitkLinear)
        registration.AddCommand(sitk.sitkIterationEvent, lambda: self.commandIteration(registration))
        out = registration.Execute(imageFixed, imageMoving)
        return out

    def registrationMethodTranslationWithSampling(self, imageFixed, imageMoving, numberOfBins=24,
                                                  samplingPercentage=0.10):
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsMattesMutualInformation(numberOfBins)
        registration.SetMetricSamplingPercentage(samplingPercentage, sitk.sitkWallClock)
        registration.SetMetricSamplingStrategy(registration.RANDOM)
        registration.SetOptimizerAsRegularStepGradientDescent(1.0, .001, 200)
        registration.SetInitialTransform(sitk.TranslationTransform(imageFixed.GetDimension()))
        registration.SetInterpolator(sitk.sitkLinear)
        registration.AddCommand(sitk.sitkIterationEvent, lambda: self.commandIteration(registration))
        out = registration.Execute(imageFixed, imageMoving)
        return out

    def registrationMethodBSpline(self, imageFixed, imageMoving):
        transformDomainMeshSize = [8] * imageMoving.GetDimension()
        tx = sitk.BSplineTransformInitializer(imageFixed,
                                              transformDomainMeshSize)
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsCorrelation()
        registration.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-5,
                                          numberOfIterations=100,
                                          maximumNumberOfCorrections=5,
                                          maximumNumberOfFunctionEvaluations=1000,
                                          costFunctionConvergenceFactor=1e+7)
        registration.SetInitialTransform(tx, True)
        registration.SetInterpolator(sitk.sitkLinear)
        registration.AddCommand(sitk.sitkIterationEvent, lambda: self.commandIteration(registration))
        out = registration.Execute(imageFixed, imageMoving)
        return out

    def registrationMethodBSpline2(self, imageFixed, imageMoving):
        transformDomainMeshSize = [10] * imageMoving.GetDimension()
        tx = sitk.BSplineTransformInitializer(imageFixed,
                                              transformDomainMeshSize)
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsMattesMutualInformation(50)
        registration.SetOptimizerAsGradientDescentLineSearch(5.0, 100,
                                                             convergenceMinimumValue=1e-4,
                                                             convergenceWindowSize=5)
        registration.SetOptimizerScalesFromPhysicalShift()
        registration.SetInitialTransform(tx)
        registration.SetInterpolator(sitk.sitkLinear)
        registration.SetShrinkFactorsPerLevel([6, 2, 1])
        registration.SetSmoothingSigmasPerLevel([6, 2, 1])
        registration.AddCommand(sitk.sitkIterationEvent, lambda: self.commandIteration(registration))
        out = registration.Execute(imageFixed, imageMoving)
        return out

    def registrationMethodBSpline3(self, imageFixed, imageMoving):
        transformDomainMeshSize = [2] * imageFixed.GetDimension()
        tx = sitk.BSplineTransformInitializer(imageFixed,
                                              transformDomainMeshSize)
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsJointHistogramMutualInformation()
        registration.SetOptimizerAsGradientDescentLineSearch(5.0,
                                                             100,
                                                             convergenceMinimumValue=1e-4,
                                                             convergenceWindowSize=5)
        registration.SetInterpolator(sitk.sitkLinear)
        registration.SetInitialTransformAsBSpline(tx,
                                                  inPlace=True,
                                                  scaleFactors=[1, 2, 5])
        registration.SetShrinkFactorsPerLevel([4, 2, 1])
        registration.SetSmoothingSigmasPerLevel([4, 2, 1])
        out = registration.Execute(imageFixed, imageMoving)
        return out

    def registationMethodDisplacement(self, imageFixed, imageMoving):
        initialTx = sitk.CenteredTransformInitializer(imageFixed, imageMoving,
                                                      sitk.AffineTransform(imageFixed.GetDimension()))
        registration = sitk.ImageRegistrationMethod()
        registration.SetShrinkFactorsPerLevel([3, 2, 1])
        registration.SetSmoothingSigmasPerLevel([2, 1, 1])
        registration.SetMetricAsJointHistogramMutualInformation(20)
        registration.MetricUseFixedImageGradientFilterOff()
        registration.SetOptimizerAsGradientDescent(learningRate=1.0,
                                                   numberOfIterations=100,
                                                   estimateLearningRate=registration.EachIteration)
        registration.SetOptimizerScalesFromPhysicalShift()
        registration.SetInitialTransform(initialTx, inPlace=True)
        registration.SetInterpolator(sitk.sitkLinear)
        out = registration.Execute(imageFixed, imageMoving)
        return out

    def registrationMethodExhaustive(self, imageFixed, imageMoving):
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
        samplePerAxis = 12
        if imageFixed.GetDimension() == 2:
            tx = sitk.Euler2DTransform()
            registration.SetOptimizerAsExhaustive([samplePerAxis // 2, 0, 0])
            registration.SetOptimizerScales([2.0 * pi / samplePerAxis, 1.0, 1.0])
        elif imageFixed.GetDimension() == 3:
            tx = sitk.Euler3DTransform()
            registration.SetOptimizerAsExhaustive(
                [samplePerAxis // 2, samplePerAxis // 2, samplePerAxis // 4, 0, 0, 0])
            registration.SetOptimizerScales(
                [2.0 * pi / samplePerAxis, 2.0 * pi / samplePerAxis, 2.0 * pi / samplePerAxis, 1.0, 1.0, 1.0])
        tx = sitk.CenteredTransformInitializer(imageFixed, imageMoving, tx)
        registration.SetInitialTransform(tx)
        registration.SetInterpolator(sitk.sitkLinear)
        registration.AddCommand(sitk.sitkIterationEvent, lambda: self.commandIteration(registration))
        out = registration.Execute(imageFixed, imageMoving)
        return out

    def getImagePath(self, filename):
        path = os.getcwd() + config.IMG_PATH + filename
        return path

    def displayResult(self, imageFixed, imageMoving, res):
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(imageFixed)
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(1)
        resampler.SetTransform(res)
        out = resampler.Execute(imageMoving)
        simg1 = sitk.Cast(sitk.RescaleIntensity(imageFixed), sitk.sitkUInt8)
        simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
        cimg = sitk.Compose(simg1, simg2, simg1 // 2. + simg2 // 2.)
        sitk.Show(cimg, "ImageRegistration1 Composition")
