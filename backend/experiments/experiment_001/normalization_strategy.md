# Landmark Normalization Strategy

## Objective

The purpose of normalization is to make the landmark coordinates independent of the hand's position in the image. This improves model consistency and reduces the effect of hand movement.

## Normalization Method

The project uses **Wrist-Relative Normalization**.

For every hand sample:

- The wrist landmark (Landmark 0) is considered as the reference point.
- The wrist coordinates (x0, y0, z0) are subtracted from every other landmark.
- After normalization, the wrist coordinates become (0, 0, 0).

Mathematically:

Normalized X = Xi - X0

Normalized Y = Yi - Y0

Normalized Z = Zi - Z0

where:

- Xi, Yi, Zi are the coordinates of the current landmark.
- X0, Y0, Z0 are the wrist coordinates.

## Advantages

- Removes dependence on hand position.
- Improves model robustness.
- Makes different hand samples easier to compare.
- Reduces unnecessary variation in the dataset.

## Output

The normalized dataset is stored as:

output/normalized_landmarks.csv