/**
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */


 /**
`CKEDITOR.config.extraPlugins: 'simage'`
`CKEDITOR.config.imageUploadURL: <INSERT URL>`
*/

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.extraPlugins = ['simage', 'emoji'];
	config.imageUploadURL = '/upload/';


};

`CKEDITOR.config.font_names =
    'Arial/Arial, Helvetica, sans-serif;' +
    'Times New Roman/Times New Roman, Times, serif;' +
    'Verdana'; `

`CKEDITOR.config.extraPlugins: 'simage'`;
`CKEDITOR.config.imageUploadURL: '/upload/'`;
`CKEDITOR.config.dataParser: func(data)`;
