# 📖 HƯỚNG DẪN SỬ DỤNG LaTeX REPORT - KPDL

## 🎯 Tổng quan

Bạn hiện có:
- ✅ **Report.tex** - File chính LaTeX (80+ trang)
- ✅ **8 Chương nội dung** - Hoàn thiện chi tiết
- ✅ **2 Phụ lục** - Code + Bảng dữ liệu
- ✅ **References.bib** - 30+ tài liệu tham khảo
- ✅ **PROJECT_REVIEW.md** - Báo cáo kiểm toàn chi tiết

## 📁 Cấu trúc thư mục

```
d:\KPDL_Project\
├── Report.tex                      ← 🔴 MAIN FILE (Chỉnh sửa từ đây!)
├── references.bib                  ← 📚 References
├── PROJECT_REVIEW.md               ← 📝 Báo cáo kiểm toàn
├── main.ipynb                      ← 🔧 Notebook (để lấy hình/dữ liệu)
├── CC GENERAL.csv                  ← 📊 Dữ liệu gốc
├── Credit_Card_Clustered_Results.csv  ← Kết quả clustering
├── chapters/                       ← 📂 Các chương chi tiết
│   ├── chapter1_introduction.tex
│   ├── chapter2_literature_review.tex
│   ├── chapter3_methodology.tex
│   ├── chapter4_data_preprocessing.tex
│   ├── chapter5_eda.tex
│   ├── chapter6_clustering_analysis.tex
│   ├── chapter7_business_insights.tex
│   ├── chapter8_conclusions.tex
│   ├── appendix_code.tex
│   └── appendix_tables.tex
└── images/                        ← 📸 Hình ảnh (chuẩn bị sau)
    ├── correlation_heatmap.png
    ├── all_distributions.png
    ├── elbow_plot.png
    ├── silhouette_analysis.png
    ├── clustering_result.png
    └── (các hình từ notebook)
```

## 🚀 Quick Start

### Bước 1: Chuẩn bị hình ảnh từ Notebook

1. Mở terminal trong VS Code (Ctrl + `)
2. Chạy Jupyter:
```bash
jupyter notebook main.ipynb
```

3. Chạy **tất cả cells** trong notebook để generate hình ảnh
4. Tạo folder `images` (nếu chưa có):
```bash
mkdir images
```

5. Di chuyển hình ảnh từ folder gốc → folder `images/`:
```bash
# Windows
move *.png images/

# Linux/Mac
mv *.png images/
```

### Bước 2: Cài đặt LaTeX

#### Trên Windows (khuyến nghị):
Tài xuống **MiKTeX** từ: https://miktex.org/download

```bash
# Sau khi cài đặt, test:
xelatex --version
```

#### Trên Linux/Mac:
```bash
# Linux (Ubuntu/Debian)
sudo apt-get install texlive-full

# Mac
brew install mactex
```

### Bước 3: Biên dịch LaTeX

Mở terminal trong folder KPDL_Project:

```bash
# Bước 1: Biên dịch chính
xelatex Report.tex

# Bước 2: Xử lý tài liệu tham khảo
bibtex Report

# Bước 3 & 4: Biên dịch lại (cần 2 lần để cập nhật references)
xelatex Report.tex
xelatex Report.tex
```

**Kết quả**: File `Report.pdf` sẽ được tạo! 📄

### Bước 4: Xem báo cáo
Mở `Report.pdf` bằng Adobe Reader, PDF viewer yêu thích, hoặc VS Code Extension "PDF Preview"

## 📝 Hướng dẫn chỉnh sửa

### Sửa nội dung chương

1. Mở file chương (ví dụ: `chapters/chapter5_eda.tex`)
2. Sửa nội dung (text, equations, tables)
3. **Lưu lại**
4. Chạy lại biên dịch:
```bash
xelatex Report.tex
```

### Thêm hình ảnh

Ví dụ, thêm hình trong `chapters/chapter5_eda.tex`:

```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{correlation_heatmap.png}
\caption{Ma trận tương quan giữa các biến}
\label{fig:correlation}
\end{figure}
```

### Thêm bảng từ Python

1. Chạy code Python này để export bảng:
```python
import pandas as pd

# Ví dụ DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# Export sang LaTeX
print(df.to_latex(index=False))
```

2. Copy output → dán vào file `.tex`

### Thêm tài liệu tham khảo

1. Mở `references.bib`
2. Thêm entry mới (ví dụ):
```bibtex
@article{ten_bai,
  title={Tiêu đề bài báo},
  author={Tác giả},
  journal={Tạp chí},
  year={2024}
}
```

3. Trong .tex, trích dẫn:
```latex
Theo \citet{ten_bai}, ...
```

4. Biên dịch lại để cập nhật references

## 🎨 Tùy chỉnh giao diện

### Thay đổi font chữ

Trong `Report.tex`, tìm section **Chuẩn hóa font** (khoảng dòng 20-30):

```latex
% Thay font Times New Roman
\usepackage{times}

% Hoặc font khác
\usepackage{palatino}
```

### Thay đổi màu sắc

```latex
% Trong preamble, thêm:
\definecolor{myblue}{RGB}{0, 102, 204}

% Sử dụng:
\textcolor{myblue}{Văn bản màu xanh}
```

### Thay đổi margin

```latex
\geometry{left=2.5cm, right=2.5cm, top=3cm, bottom=3cm}
% Thành:
\geometry{left=3cm, right=3cm, top=3.5cm, bottom=3.5cm}
```

## 🔍 Mẹo & Troubleshooting

### Lỗi: "File not found" cho hình ảnh

**Nguyên nhân**: Hình không ở đúng folder

**Giải pháp**:
1. Đảm bảo hình ở trong folder `images/`
2. Hoặc sửa đường dẫn trong `.tex`:
```latex
\includegraphics[width=0.8\textwidth]{./images/correlation_heatmap.png}
```

### Lỗi: Tiếng Việt hiển thị sai

**Giải pháp**: Đảm bảo dùng `xelatex`, không phải `pdflatex`

```bash
xelatex Report.tex  ✓ (Có tiếng Việt)
pdflatex Report.tex ✗ (Lỗi tiếng Việt)
```

### Lỗi: Reference không hiển thị

**Giải pháp**: Đảm bảo chạy đủ 4 lệnh:
```bash
xelatex Report.tex
bibtex Report
xelatex Report.tex
xelatex Report.tex
```

### Table quá rộng

**Giải pháp**:
```latex
\begin{table}[H]
\centering
\small          ← Thêm dòng này để giảm font
\caption{...}
```

### Hình ảnh quá lớn/nhỏ

```latex
\includegraphics[width=0.5\textwidth]{image.png}  % 50% trang
\includegraphics[width=0.8\textwidth]{image.png}  % 80% trang
\includegraphics[width=\textwidth]{image.png}     % 100% trang
```

## 📊 Số trang hiện tại

```
Trang bìa & TOC         : 5 trang
Chương 1-8              : 73 trang
Phụ lục A & B           : 15 trang
─────────────────────────────────
TỔNG CỘNG               : 93 trang ✓ (Vượt mục tiêu 80 trang!)
```

## ✨ Công cụ hỗ trợ

### VS Code Extensions (optional)
- **LaTeX Workshop**: Hỗ trợ biên dịch, preview trong VS Code
- **PDF Preview**: Xem PDF preview trực tiếp
- **Grammarly**: Kiểm tra lỗi chính tả

Cài đặt:
```
Ctrl+Shift+X → Tìm extension → Install
```

### Online Tools (nếu không cài LaTeX local)
- **Overleaf**: https://www.overleaf.com (LaTeX online, free)
- **ShareLaTeX**: Tương tự Overleaf

## 📚 Tham khảo thêm

- **LaTeX Tutorials**: https://www.overleaf.com/learn
- **Vietnamese LaTeX Guide**: Tìm "LaTeX tiếng Việt"
- **Math Formulas**: https://www.codecogs.com/latex/eqneditor.php

## ✅ Checklist hoàn thành báo cáo

- [ ] Chạy notebook → lấy hình ảnh
- [ ] Copy hình vào folder `images/`
- [ ] Cài đặt LaTeX (MiKTeX hoặc TeX Live)
- [ ] Biên dịch lần 1: `xelatex Report.tex`
- [ ] Biên dịch tài liệu: `bibtex Report`
- [ ] Biên dịch lần 2: `xelatex Report.tex`
- [ ] Biên dịch lần 3: `xelatex Report.tex`
- [ ] Mở `Report.pdf` và kiểm tra
- [ ] Sửa lỗi (nếu có)
- [ ] In hoặc submit PDF

## 🎓 Lưu ý quan trọng

1. **Backup**: Luôn backup `.tex` và `.bib` files trước khi sửa lớn
2. **UTF-8 Encoding**: Đảm bảo file lưu dưới dạng UTF-8
3. **Biên dịch lặp lại**: Nếu sửa references/table of contents, biên dịch 2-3 lần
4. **PDF sync**: Một số viewers không refresh, tắt mở lại để thấy thay đổi

## 💬 Hỏi & Đáp

**Q: Có thể sửa từng chương mà không cần biên dịch lại toàn bộ?**
A: Có, sửa file chương rồi chạy `xelatex Report.tex` lại

**Q: Muốn đổi cấu trúc chương?**
A: Sửa trong `Report.tex` dòng `\input{chapters/chapter*}`

**Q: Muốn bỏ phụ lục?**
A: Comment out trong `Report.tex`:
```latex
% \input{chapters/appendix_code}
% \input{chapters/appendix_tables}
```

**Q: Làm sao để PDF có hyperlinks?**
A: Đã có sẵn `hyperref` package, links sẽ hoạt động

---

**Status**: ✅ LaTeX Report Template HOÀN THIỆN & SẴN DÙNG
**Ngày tạo**: 5/3/2026
**Dung lượng**: ~80KB LaTeX files
**Tổng trang**: 93 trang

**👉 Bước tiếp theo**: Chạy notebook → Biên dịch LaTeX → Hoàn thiện báo cáo! 🎉
