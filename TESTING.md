# Testing Guide

## Quick Test

Чтобы быстро проверить, работает ли депикселизация:

```bash
# Запустить автоматический тест
python3 test_run.py
```

Этот скрипт:
1. Создаст тестовые изображения
2. Запустит депикселизацию
3. Проверит результаты
4. Выведет отчет

## Manual Test

### Шаг 1: Создать тестовое изображение

```bash
python3 tool_gen_pixelated.py \
    -i images/testimages/testimage3_pixels.png \
    -o test_pixelated.png \
    --blocksize 5
```

### Шаг 2: Проверить детекцию блоков

```bash
python3 tool_show_boxes.py \
    -p test_pixelated.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png
```

**Проверьте:**
- Блоки должны быть четкими прямоугольниками
- Одинаковый размер блоков
- Нет фрагментации

### Шаг 3: Запустить депикселизацию

```bash
python3 depix.py \
    -p test_pixelated.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png \
    -o test_output.png
```

**Ожидаемый вывод:**
```
INFO - Loading pixelated image from test_pixelated.png
INFO - Loading search image from ...
INFO - Found X same color rectangles
INFO - Y rectangles left after moot filter
INFO - Found Z different rectangle sizes
INFO - Finding matches in search image
INFO - Progress: 50/X blocks processed (XX.X%)
INFO - [A straight matches | B multiple matches]
INFO - Successfully saved output image to: test_output.png
```

### Шаг 4: Проверить результат

```bash
# Открыть изображения для сравнения
open test_pixelated.png test_output.png

# Или на Linux
eog test_pixelated.png test_output.png
```

## Unit Tests

Запустить юнит-тесты:

```bash
python3 -m pytest tests/test_depix.py -v
```

Ожидаемый вывод:
```
tests/test_depix.py::TestRectangle::test_rectangle_creation PASSED
tests/test_depix.py::TestRectangle::test_rectangle_area PASSED
tests/test_depix.py::TestColorRectangle::test_color_rectangle_creation PASSED
tests/test_depix.py::TestHelpers::test_check_color_valid PASSED
...
```

## Проверка отдельных компонентов

### Тест LoadedImage

```python
from depixlib.LoadedImage import LoadedImage

img = LoadedImage('test.png')
print(f"Size: {img.width}x{img.height}")
print(f"Pixel at (0,0): {img.imageData[0][0]}")
```

### Тест Rectangle

```python
from depixlib.Rectangle import Rectangle, ColorRectangle

rect = Rectangle((0, 0), (10, 10))
print(f"Area: {rect.area}")
print(f"Contains (5,5): {rect.contains_point(5, 5)}")

color_rect = ColorRectangle((255, 0, 0), (0, 0), (5, 5))
print(f"Color: {color_rect.color}")
```

### Тест Block Detection

```python
from depixlib.LoadedImage import LoadedImage
from depixlib.Rectangle import Rectangle
from depixlib.functions import findSameColorSubRectangles

img = LoadedImage('pixelated.png')
rect = Rectangle((0, 0), (img.width-1, img.height-1))
blocks = findSameColorSubRectangles(img, rect)
print(f"Found {len(blocks)} blocks")
```

## Диагностика проблем

### Проблема: Нет matches

**Проверка 1: Размер изображений**
```python
from PIL import Image

pix = Image.open('pixelated.png')
search = Image.open('search.png')
print(f"Pixelated: {pix.size}")
print(f"Search: {search.size}")
# Search должен быть больше pixelated
```

**Проверка 2: Детекция блоков**
```bash
python3 tool_show_boxes.py -p pixelated.png -s search.png
# Должны быть четкие блоки
```

**Проверка 3: Цвета**
```python
from PIL import Image
import numpy as np

pix = np.array(Image.open('pixelated.png'))
search = np.array(Image.open('search.png'))

print(f"Pixelated color range: {pix.min()}-{pix.max()}")
print(f"Search color range: {search.min()}-{search.max()}")
```

### Проблема: Плохое качество

**Тест 1: Оба метода averaging**
```bash
# Gamma
python3 depix.py -p pix.png -s search.png -a gammacorrected -o out1.png

# Linear  
python3 depix.py -p pix.png -s search.png -a linear -o out2.png

# Сравнить
```

**Тест 2: С фильтром фона**
```bash
python3 depix.py -p pix.png -s search.png -b 255,255,255 -o out3.png
```

## Regression Tests

Создать набор тестовых случаев:

```bash
# test_suite.sh
#!/bin/bash

echo "Running Depix Test Suite..."

# Test 1: Basic depixelization
python3 depix.py \
    -p images/testimages/testimage3_pixels.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png \
    -o test1_output.png
test1=$?

# Test 2: Linear averaging
python3 depix.py \
    -p images/testimages/sublime_screenshot_pixels_gimp.png \
    -s images/searchimages/debruin_sublime_Linux_small.png \
    -a linear \
    -o test2_output.png
test2=$?

# Report
if [ $test1 -eq 0 ] && [ $test2 -eq 0 ]; then
    echo "✓ All tests passed"
    exit 0
else
    echo "✗ Some tests failed"
    exit 1
fi
```

## Performance Testing

### Измерение времени

```bash
time python3 depix.py -p large.png -s search.png -o out.png
```

### Измерение памяти

```bash
/usr/bin/time -v python3 depix.py -p large.png -s search.png -o out.png
```

### Профилирование

```python
import cProfile
import pstats

# Profile the main function
cProfile.run('main()', 'depix_profile')

# Analyze results
p = pstats.Stats('depix_profile')
p.sort_stats('cumulative')
p.print_stats(20)
```

## Continuous Integration

Для GitHub Actions добавьте `.github/workflows/test.yml`:

```yaml
name: Test Depix

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run tests
      run: python3 test_run.py
```

## Отчет об ошибках

При обнаружении ошибки, включите:

1. **Версия Python**: `python3 --version`
2. **Версии пакетов**: `pip list | grep -E "(Pillow|numpy|opencv)"`
3. **Команда**: Полная команда, которую вы запустили
4. **Вывод**: Полный вывод с ошибками
5. **Изображения**: Если возможно, приложите pixelated.png и search.png

Пример:
```
Python: 3.9.5
Pillow: 9.0.0
numpy: 1.21.0
opencv-python: 4.5.5

Command:
python3 depix.py -p test.png -s search.png -o out.png

Error:
Traceback (most recent call last):
  ...
```
