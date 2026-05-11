const puppeteer = require('puppeteer');
const path = require('path');

async function generatePDF() {
    console.log('Inicializando Puppeteer...');
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();
    const htmlPath = path.join(__dirname, 'dossie_perus.html');
    const pdfPath = path.join(__dirname, 'dossie_perus.pdf');
    const fileUrl = `file://${htmlPath.replace(/\\/g, '/')}`;
    console.log('Carregando:', fileUrl);
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 3000));
    console.log('Gerando PDF...');
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true,
        margin: { top: '0', bottom: '0', left: '0', right: '0' }
    });
    await browser.close();
    console.log('PDF gerado com sucesso:', pdfPath);
}

generatePDF().catch(console.error);
