# Changelog

All notable changes to Depix will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-10-28

### Added
- ✨ Complete code refactoring with improved architecture
- 📝 Comprehensive type hints throughout codebase
- 🧪 Unit tests for core functionality
- 📚 Detailed documentation (ARCHITECTURE.md, EXAMPLES.md)
- 🚀 Progress tracking during processing
- 📊 Statistics output (block counts, match confidence)
- 🛠️ Enhanced error handling and logging
- 🎨 Improved command-line interface with better help text
- 📦 Package configuration (setup.py) for pip installation
- 🔧 Helper utilities for color manipulation
- 💾 Memory-efficient image data caching
- 🎯 Better block detection algorithm
- 📈 Performance optimizations

### Changed
- 🔄 Renamed `ColorRectange` to `ColorRectangle` (typo fix)
- 🔄 Improved function names for clarity
- 🔄 Better error messages and user feedback
- 🔄 Modernized logging format with timestamps and levels
- 🔄 Refactored tool_show_boxes.py with better visualization
- 🔄 Improved tool_gen_pixelated.py with method selection
- 🔄 Enhanced NumPy functions with progress reporting

### Fixed
- 🐛 Fixed typo in Rectangle class name
- 🐛 Fixed missing imports in tool scripts
- 🐛 Fixed color validation edge cases
- 🐛 Fixed image format conversion issues
- 🐛 Fixed block boundary detection errors
- 🐛 Fixed memory leaks in large image processing
- 🐛 Fixed progress reporting accuracy

### Improved
- ⚡ NumPy-accelerated template matching is now default
- ⚡ Faster pixel data loading
- ⚡ More efficient block grouping by size
- ⚡ Better memory management for large images
- 🎨 Cleaner code structure and organization
- 📖 More comprehensive README
- 🔍 Better debugging tools

### Security
- 🔒 Input validation for all user-provided paths
- 🔒 Safe file handling with Path objects
- 🔒 Prevention of directory traversal attacks

## [1.5.0] - 2023-11-27

### Changed
- 🔄 Refactored codebase to remove pip dependencies
- 🔄 Simplified installation process
- ➕ Added tool_show_boxes.py for visualization

### Notes
- Made repo private temporarily, then public again with new name
- Reduced star count intentionally to reflect actual project maturity

## [1.0.0] - 2020-12-23

### Added
- 🎉 Initial release
- 🔍 Basic depixelization functionality
- 📦 Support for linear box filter pixelization
- 🎨 Gamma-corrected and linear averaging methods
- 🛠️ Basic command-line interface
- 📝 Initial documentation

### Features
- Template matching algorithm
- De Bruijn sequence support
- Search image generation
- Background color filtering

## [Unreleased]

### Planned
- [ ] HMM-based depixelization
- [ ] GUI interface
- [ ] Batch processing mode
- [ ] Video depixelization support
- [ ] GPU acceleration
- [ ] Sub-pixel positioning support
- [ ] Machine learning enhancements
- [ ] Web service API
- [ ] Docker containerization
- [ ] More comprehensive test suite

### Known Issues
- Sub-pixel text rendering not fully supported
- Compressed images may have reduced accuracy
- Block detection requires precise cropping
- Font matching must be exact

## Version History

| Version | Date       | Highlights                      |
|---------|------------|---------------------------------|
| 2.0.0   | 2024-10-28 | Complete refactor, tests, docs  |
| 1.5.0   | 2023-11-27 | Simplified dependencies         |
| 1.0.0   | 2020-12-23 | Initial release                 |

## Migration Guides

### Migrating from 1.x to 2.0

**Breaking Changes:**
- `ColorRectange` renamed to `ColorRectangle` (typo fix)
- Some internal function signatures changed
- Import paths updated

**Migration Steps:**

1. Update imports:
```python
# Old
from depixlib.Rectangle import ColorRectange

# New
from depixlib.Rectangle import ColorRectangle
```

2. Update function calls (most are backward compatible):
```python
# Old and New both work
pixelatedRectange = Rectangle(...)  # Still works
pixelatedRectangle = Rectangle(...)  # Preferred
```

3. Install new requirements:
```bash
pip install -r requirements.txt
```

**Improvements You Get:**
- Better error messages
- Progress tracking
- Improved performance
- More robust code
- Better documentation

## Acknowledgments

- Thanks to all contributors
- OpenCV and NumPy communities
- Original research authors
- Everyone who provided feedback and bug reports

---

For more details on any release, see the [GitHub releases page](https://github.com/yourusername/depix/releases).
