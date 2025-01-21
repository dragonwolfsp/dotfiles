# Nao - NVDA 高级 OCR

* 作者：Alessandro Albano、Davide De Carne、Simone Dal Maso
* 下载[稳定版][1]
* NVDA 兼容性：2019.3 及以后

Nao(NVDA Advanced OCR) 是一个 NVDA 插件，该插件改进了 Windows 的内置 OCR 功能。
虽然 NVDA 本身可以使用 Windows OCR 来识别屏幕，但 NAO 能够对保存在硬盘驱动器或 USB 设备上的文件进行 OCR。 
使用 NVDA + Shift + R 识别任何类型的图片或 PDF 文件！
您只需将焦点/光标放在您想要识别的文件上，无需打开，直接按下 NVDA + Shift + r 即可。
该文档将被识别，完成后会出现一个简单的识别结果窗口，您可以阅读、保存、查找或复制识别结果到剪贴板。
Nao 也能够处理多页 PDF，所以，如果您有一个无法阅读的扫描版文档，请不要担心， Windows OCR 能够协助你阅读它。

## 系统要求

该插件适用于内置了 OCR 功能的 Windows 10 和 Windows 11 系统。
Nao 与 NVDA 版本 2019.3 兼容，所以也不要使用旧版本的屏幕阅读器。
另外请注意，Nao 可与 Windows 资源管理器、桌面、 Total Commander 或  xplorer² 文件管理器配合使用；不要使用 7zip 或 Winrar 等其他软件，因为这些软件不在本插件的支持范围内。
For e-mail attachments, it also works with Microsoft Outlook 2016 or beyond.

## 功能和快捷键

* NVDA + Shift + R：从文件管理器中识别任何类型的图像和 PDF；
  * PgUp / PgDown：在多页文档的实际页面之间翻页。
  * Ctrl + S：将文档保存为 nao-document 格式。您可以使用 NVDA + Shift + R 直接打开该文档。
  * P：在多页文档中读出与光标位置相对应的页码。
  * L：光标所在位置的行号，基于当前页。
  * Shift + L：光标所在位置的行号，基于整个文档。
  * G：直接跳转到某页。
  * c：将所有文本复制到剪贴板。
  * s：以文本格式保存文档的副本。 
  * f：查找文本并读出查找结果前后的内容。
  * 译者注： 同时支持 F3/Shift+F3的前 / 后一个查找结果跳转。
* NVDA + Shift + Ctrl + R：全屏截图并识别。
  * 注： 您可以使用 NVDA 的标准命令来导航全屏识别结果的窗口。例如，您可以使用箭头键移动到某个按钮，并按下 Enter 键来激活它。您也可以使用 NVDA + 小键盘斜杠，把鼠标移到相应的位置，然后执行左/右键单击。


请注意，您可以轻松地从 NVDA 的按键与手势对话框中自定义 Nao 的快捷键。打开 NVDA 菜单，转到选项，然后从该子菜单中选择“按键与手势”。注意，此功能不是全局性的，仅当 Nao 可以进行 ocr 时才有效。因此，只有在桌面、文件浏览器、Total Commander 或 Xplorer 中才可以自定义快捷键。

在识别过程中，如果时间过长您可以随时终止 Ocr ，只需从进度窗口中按“取消”按钮即可；此窗口还显示 OCR 的进度信息，每 5 秒更新一次。您可以使用 NVDA + u 设置如何读出进度。

您可以在 NVDA 菜单的工具菜单下找到一个名为 Nao 的子菜单。目前它包含“捐赠”、“检测更新”等入口，以后可能会包含更多功能。
* Select file: allow you to select a file for processing without using a shortkey.
* Make a donation: it's self-explanatory, if you feel like it we'll be very happy!
* Nao Website: brings you to the homepage of Nao.
* Git: brings you to the source codeò where you can check it, make commit or open an issue.
* Check for updates: queries the server for a new version of Nao.
* Empty cache: If you encounter problems with the add-on, receive error messages or find it slow, clear your cache to resolve the issue.


## 支持和捐赠

Nao是完全免费的插件。它是开发者利用闲暇时间开发的。
对于您的贡献我们将不胜感激！
如果您认为我们的插件很好并改善了您的生活，请<a href="https://nvda-nao.org/donate">考虑给我们捐赠。</a>

您想报告错误、建议增加新功能、亦或想翻译该插件吗？只需发送电子邮件至 support@nvda-nao.org，我们很乐意为您提供帮助。


## 更新历史
### 2025.1
* NVDA version 2025.1 compatibility
* Implement OCR recognition on the selected attachment of an opened Outlook message, from outlook 2016 and beyond
* Added finnish translation
### 2024.1
* NVDA version 2024.1 compatibility
### 2023.1.1
* Compatibility with NVDA version 2023.3 restored
* New NVDA + Ctrl + Shift + W hotkey take a screen shot of the current window and recognize it
* Added Brazilian Portuguese translations
* Security Fix on Secure Screens
* NAO tools menu removed on Secure Screens
* Documents cache removed on Secure Screens
* NAO website and Git repository links added on NAO tools menu
### 2023.1
* NVDA version 2023.1 compatibility
### 2022.1.3
* NVDA version 2022.1 compatibility
* Simplified Chinese and French translations updated
* Spanish documentation updated

### 2022.1.2
* 支持 nao-document 文件格式的保存/加载功能。
* 文件缓存功能可以保存识别数据以加快下次打开的速度。如果在缓存中找到文件，则不会再次执行识别，而是从缓存中打开（识别参数必须匹配）。
* 将文档的最后阅读位置保存在缓存元数据中。
* 自动清除文档缓存。
* 在工具菜单中手动清除缓存。
* 支持直接从 Windows 资源管理器的“压缩文件夹”中识别文件。
* 更完善的无效文件检查。
* 使用不同的文件选择方案更好地兼容 Windows 资源管理器：首先尝试在 NVDA 中使用 Shell.Application，然后在 PowerShell 中尝试 Shell.Application，最后是手动浏览。
* OCR 引擎在整个识别过程中保持语言设置不变，即使在多页识别过程中更改了语言设置也不影响识别过程。
* OCR 队列可识别多个来源。
* 在文档最后一页，按 PgDown 跳转到文档末尾。
* 工具使用 Windows 临时文件夹来执行转换，而不是插件文件夹（在 NVDA 便携版上性能更好）。
* 罗马尼亚语翻译和简体中文翻译的更新。
### 2022.1.1
* 支持 DjVu 文件格式。
* 支持多页 tiff 文件。
* 针对中文操作系统的 PDF 编码错误修复。
* 在 NVDA菜单的工具子菜单下，增加了“检测更新”入口。
* 兼容标志从 NVDA 2019.3 开始。


### 2022.1
* 插件自动更新。
* 更新了西班牙语和法语翻译。

### 2021.2
* pdf和图片的OCR结果使用一个新的文本窗口显示，并且增加了一些易于操作的热键。
* 支持 Xplorer 文件管理器。
* Nao 的快捷键可从 NVDA 的按键与手势对话框中进行自定义。
* Nao 仅在可能的情况下运行，因此如果您在不受支持的环境下，插件将会忽略相应的快捷键；这解决了 Excel 和 Word 用户无法使用 NVDA +Shift +r 的问题，因为在过去它被 Nao 错误地拦截了。
* 只需按进度窗口上的“取消”按钮即可中止 Ocr 过程。
* 添加了土耳其语、俄语、西班牙语、中文和法语翻译。
* 用户可以对该项目进行捐赠。
* 修复了文件名中的某些字符会导致 Ocr 无法正常工作的错误。

### 2021.1
* 第一个公开版本！

[1]: https://nvda-nao.org/download