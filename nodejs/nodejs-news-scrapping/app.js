const { default: axios } = require('axios');
const express = require('express');
const app = express();
const cheerio = require('cheerio');

const PORT = process.env.port || 3000;

const website = 'https://news.sky.com';

try {
    axios(website).then((response) => {
        // get a html data
        // const html = response.data;
        // console.log(html);

        const data = response.data;
        const $ = cheerio.load(data);

        let content = [];

        $('.sdc-site-tile__headline', data).each(function() {
            const title = $(this).text();
            const url = $(this).find('a').attr('href');

            content.push({
                title,
                url
            });

            app.get('/', (req, res) => {
                res.json(content);
            });
        });
    });
} catch(error) {
    console.log(error, error.message);
}

app.listen(PORT, () => {
    console.log(`server is running on PORT: ${PORT}`);
});

