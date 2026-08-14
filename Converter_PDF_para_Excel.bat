@echo off
title Conversor de PDF para Excel (Offline)
color 0A
cls
echo ====================================================
echo            CONVERSOR DE PDF PARA EXCEL              
echo                (100%% Offline e Local)               
echo ====================================================
echo.

if exist "dist\Converter_PDF_para_Excel.exe" (
    if "%~1"=="" (
        echo Abrindo janela de selecao de arquivo...
        "dist\Converter_PDF_para_Excel.exe" --gui
    ) else (
        echo Processando arquivo carregado: %~1
        "dist\Converter_PDF_para_Excel.exe" -f "%~1"
    )
) else (
    if "%~1"=="" (
        echo Abrindo janela de selecao de arquivo...
        python -m pdf_to_sheet.cli --gui
    ) else (
        echo Processando arquivo carregado: %~1
        python -m pdf_to_sheet.cli -f "%~1"
    )
)

echo.
echo Conversao concluida!
pause
