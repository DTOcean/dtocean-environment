# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- Added change log and CI files.

### Changed

- Changed name of "operation and maintenance" data folder to "maintenance" to
  avoid bug in constructor when unzipping file paths containing exactly 100
  characters.

### Fixed

- Fixed typos in data (csv) files.
- Fixed all NaNs going to numpy functions (which issue warnings).
- Fixed use of depreciated pandas.reindex_axis.

## [1.0.0] - 2017-01-05

### Added

- Initial import of dtocean-environmental from SETIS.

### Changed

- Changed package name from dtocean-environmental to dtocean-environment.
