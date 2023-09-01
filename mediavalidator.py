import numpy as np
from joblib import dump, load
from mando import command, main
from skimage import io, exposure
from skimage.feature import hog
from skimage.transform import rescale
from sklearn.metrics.pairwise import pairwise_kernels
from sklearnex import patch_sklearn
from glob import glob

patch_sklearn(global_patch=True)
# defining constants
CORRECTION_FACTOR = 2
TARGET_SIZE = (256, 256)
FEATURES_DIR = "features"
MAX_FEATURE_SIZE = 328888
MODEL_PATH = "models/hog_mixture_ratio_0_01-03-2023 11-01-11_model.sav"
TIME_THRESHOLD = 128.278211 - 1e-100
ALPHA = 0.05
GAMMA = 0.5
DEGREE = 3


def kernel(x, y):
    return np.clip(
        ALPHA * pairwise_kernels(x, y, metric="rbf", gamma=GAMMA)
        + (1 - ALPHA) * pairwise_kernels(x, y, metric="poly", degree=DEGREE),
        -2e100,
        2e100,
    )


def predict(model, x):
    dataset = np.load("features/dataset_reduced.csv_HOG_.npy").astype(np.float64)
    x_train = np.delete(dataset, [-3, -2, -1], axis=1)
    max_d = max(x.shape[1], x_train.shape[1])
    kernel_matrix = kernel(
        np.pad(
            x,
            pad_width=((0, 0), (0, max_d - x.shape[1])),
            mode="constant",
            constant_values=0,
        ),
        np.pad(
            x_train,
            pad_width=((0, 0), (0, max_d - x_train.shape[1])),
            mode="constant",
            constant_values=0,
        ),
    )
    return model.predict(kernel_matrix)


def descriptor(image):
    # rescale instead of resizing to avoid distortion
    max_size = max(image.shape)
    target_scale = min(TARGET_SIZE) / max_size
    image = rescale(image, target_scale, anti_aliasing=True, multichannel=True)

    # adjust gamma to improve contrast
    image = exposure.adjust_gamma(image, CORRECTION_FACTOR)

    # extract features
    features = hog(image, feature_vector=True, channel_axis=2)
    # pad features to max size
    features = np.pad(
        features,
        pad_width=(0, MAX_FEATURE_SIZE - len(features)),
        mode="constant",
        constant_values=0,
    )
    return features


@command
def validate(filenames):
    # load each image as numpy array
    imageset = np.array(
        list(map(lambda filename: descriptor(io.imread(filename)), filenames))
    )
    model = load(open(MODEL_PATH, "rb"))
    model.kernel = "precomputed"
    survtime = predict(model, imageset)
    print(f"Survival time: {survtime}")
    valid = survtime > TIME_THRESHOLD
    print(f"Prediction: {valid}")
    print("valid" if valid else "invalid")
    return valid

if __name__ == "__main__":
    main()
