--[[init.lua]]

vim.g.mapleader = " "
vim.g.localleader = "\\"

vim.cmd([[
	autocmd VimEnter * NERDTree
]])


--[imports]
require('set')
--require('opts')
--require('keys')
require('plugins')



