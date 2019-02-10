from src.Service.ManageImage import ManageImage
import config
import sys

a = sys.argv
if len(sys.argv) > 1:
    transformation = str(sys.argv[1])
else:
    transformation = 'BSpline'

manage = ManageImage()

imageFixedPath = manage.getImagePath(config.IMAGES[0])
imageMovingPath = manage.getImagePath(config.IMAGES[1])

imageFixed = manage.readImage(imageFixedPath)
imageMoving = manage.readImage(imageMovingPath)

# processing, displaying required imageJ in Users/User/Fiji.app otherwise will throw error
if transformation == "translation":
    resTranslation = manage.registrationMethodTranslation(imageFixed, imageMoving)
    manage.displayResult(imageFixed, imageMoving, resTranslation)
elif transformation == 'translation2':
    resTranslation2 = manage.registrationMethodTranslation2(imageFixed, imageMoving)
    manage.displayResult(imageFixed, imageMoving, resTranslation2)
elif transformation == 'translation+sampling':
    resTranslation3 = manage.registrationMethodTranslationWithSampling(imageFixed, imageMoving)
    manage.displayResult(imageFixed, imageMoving, resTranslation3)
elif transformation == 'centered':
    resTranslationCentered = manage.registrationMethodCenteredTransform(imageFixed, imageMoving) #trwa najdluzej
    manage.displayResult(imageFixed, imageMoving, resTranslationCentered)
elif transformation == 'Exhaustive':
    resExhaustive = manage.registrationMethodExhaustive(imageFixed, imageMoving)
    manage.displayResult(imageFixed, imageMoving, resExhaustive)
elif transformation == 'BSpline':
    resBSpline = manage.registrationMethodBSpline(imageFixed, imageMoving)
    manage.displayResult(imageFixed, imageMoving, resBSpline)
elif transformation == 'BSpline2':
    resBSpline2 = manage.registrationMethodBSpline2(imageFixed, imageMoving)
    manage.displayResult(imageFixed, imageMoving, resBSpline2)
elif transformation == 'BSpline3':
    resBSpline3 = manage.registrationMethodBSpline3(imageFixed, imageMoving)
    manage.displayResult(imageFixed, imageMoving, resBSpline3)
else:
    print('unsupported!')
