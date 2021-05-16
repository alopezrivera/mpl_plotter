# Set running directory to project root directory
cd ..; cd ..;
# Run coverage
coverage run -m unittest discover;
# Generate badge
coverage-badge -o coverage.svg;
# Coverage destination
$CovDest = "tests\coverage";

# Remove previous .coverage and badge
$CovName = "$CovDest\.coverage";
$BadgeName = "$CovDest\coverage.svg";
if (Test-Path $CovName) {
  Remove-Item $CovName;
}
if (Test-Path $BadgeName) {
  Remove-Item $BadgeName;
}

# Move .coverage and badge to \coverage
Move-Item -Path ".coverage" -Destination $CovDest;
Move-Item -Path "coverage.svg" -Destination $CovDest;

