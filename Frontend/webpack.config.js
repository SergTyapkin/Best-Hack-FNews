const path = require('path');

const webpack = require('webpack');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist'),
        publicPath: '/'
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: 'src/index.html',
            favicon: 'src/res/favicon.ico'
        }),
        new VueLoaderPlugin(),
        new webpack.DefinePlugin({
            VUE_OPTIONS_API: true,
            VUE_PROD_DEVTOOLS: true,
        })
    ],
    devServer: {
        port: 9000,
        historyApiFallback: {
            rewrites: [
                {
                    from: /.(js|png|jpg|jpeg|gif|svg|ico)$/,
                    to: (context) => {
                        const path = context.parsedUrl.pathname.split('/')
                        return `/${path[path.length - 1]}`
                    }
                },
                { from: /^\/#/, to: '/index.html' },
            ]
        },
        proxy: {
            '/api': {
                target: '',
                secure: false,
                changeOrigin: true
            }
        }
    },
    resolve: {
        extensions: ['.ts', '.tsx', '.js'],
    },
    module: {
        rules: [
            {
              test: /\.vue$/,
              use: [
                  'vue-loader',
              ]
            },
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader',
                ],
            },
            {
                test: /\.(png|jpg|jpeg|gif|svg|ico)$/,
                loader: 'file-loader'
            },
            {
                test: /\.worker.js$/,
                use: { loader: 'worker-loader' }
            },
            {
                test: /\.styl(us)?$/,
                use: [
                    'style-loader',
                    'css-loader',
                    'stylus-loader'
                ]
            },
            {
                test: /\.tsx?$/,
                loader: 'ts-loader',
            },
            {
                test :/\.exec\.js$/,
                use: 'script-loader'
            }
        ],
    }
};
