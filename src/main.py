from src.Service.ManageImage import ManageImage
import config

manage = ManageImage()

imageFixedPath = manage.getImagePath(config.IMAGES[0])
imageMovingPath = manage.getImagePath(config.IMAGES[1])
# reading imgs
imageFixed = manage.readImage(imageFixedPath)
imageMoving = manage.readImage(imageMovingPath)

# processing
resTranslation = manage.registrationMethodTranslation(imageFixed, imageMoving)
resTranslation2 = manage.registrationMethodTranslation2(imageFixed, imageMoving)
resTranslation3 = manage.registrationMethodTranslationWithSampling(imageFixed, imageMoving)
resTranslationCentered = manage.registrationMethodCenteredTransform(imageFixed, imageMoving)
resBSpline = manage.registrationMethodBSpline(imageFixed, imageMoving)
resBSpline2 = manage.registrationMethodBSpline2(imageFixed, imageMoving)
resBSpline3 = manage.registrationMethodBSpline3(imageFixed, imageMoving)
resExhaustive = manage.registrationMethodExhaustive(imageFixed, imageMoving)

# displaying required imageJ
manage.displayResult(imageFixed, imageMoving, resTranslation)
manage.displayResult(imageFixed, imageMoving, resTranslation2)
manage.displayResult(imageFixed, imageMoving, resTranslation3)
manage.displayResult(imageFixed, imageMoving, resTranslationCentered)
manage.displayResult(imageFixed, imageMoving, resBSpline)
manage.displayResult(imageFixed, imageMoving, resBSpline2)
manage.displayResult(imageFixed, imageMoving, resBSpline3)
manage.displayResult(imageFixed, imageMoving, resExhaustive)

