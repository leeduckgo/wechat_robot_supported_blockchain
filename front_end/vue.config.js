
module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://ahasmarter.com/',
                pathRewrite: {
                    '^/': ''
                },
                changeOrigin: true
            }
        },
        overlay: {
            warnings: false,
            errors: false
        }
    },
    lintOnSave: false,
    productionSourceMap: false
}