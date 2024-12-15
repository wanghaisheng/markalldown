const fs = require('fs');
const path = require('path');

const locales = ['', 'fr', 'zh', 'es', 'de'];  // Define available locales
const baseDir = path.join(__dirname, '/');  // Base directory where the files are located
const baseUrl = 'https://feelingchart.heytcm.com';  // Your base URL

// Function to list all HTML files recursively in a given directory
function listHtmlFiles(dir) {
    return fs.readdirSync(dir).reduce((files, file) => {
        const filePath = path.join(dir, file);
        const isDirectory = fs.statSync(filePath).isDirectory();
        if (isDirectory) {
            return files.concat(listHtmlFiles(filePath));
        }
        if (path.extname(file) === '.html') {
            return files.concat([filePath]);
        }
        return files;
    }, []);
}

// Generate a list of all HTML files across all language folders
const allHtmlFiles = locales.flatMap(locale => {
    const localeDir = path.join(baseDir, locale);
    return listHtmlFiles(localeDir).map(file => path.join(locale, path.relative(localeDir, file)).replace(/\\+/g, '/'));
});

// Build the sitemap, ensuring that index.html files do not include /index.html in the URL
const sitemap = [
    { loc: '/', changefreq: 'daily', priority: '1.0' },
    ...allHtmlFiles.map(file => {
        const fileWithoutExtension = file.replace('.html', '');
        // If the file is index.html, remove it from the URL path
        const loc = fileWithoutExtension.endsWith('index') 
            ? `/${fileWithoutExtension.split('/').slice(0, -1).join('/')}`  // Strip index.html from the URL path
            : `/${fileWithoutExtension}`;
        return {
            loc,
            changefreq: 'weekly',
            priority: '0.9',
        };
    })
];

// Generate the sitemap XML structure
const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    ${sitemap.map(item => `    <url>
        <loc>${baseUrl}${item.loc}</loc>
        <changefreq>${item.changefreq}</changefreq>
        <priority>${item.priority}</priority>
    </url>`).join('\n')}
</urlset>`;

fs.writeFileSync('sitemap.xml', sitemapXml);  // Save the generated sitemap to a file

console.log('Sitemap has been generated and saved to sitemap.xml');
