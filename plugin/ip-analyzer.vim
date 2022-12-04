" environment check ================
let g:ip_analyzer_plugin_path = expand('<sfile>:p:h:h')
function! s:env_check()
  if !exists('g:ip_analyzer_virtual_python_path')
    if empty(glob(g:ip_analyzer_plugin_path.'/virtual_environment_info.vim'))
      echoerr 'ip-analyzer.vim: please run "pipenv run python install.py" at this plugin folder first'
      return 0
    else
      try
        exe 'so '.g:ip_analyzer_plugin_path.'/virtual_environment_info.vim'
      catch
        echoerr 'ip-analyzer.vim: error setting virtual_environment_info, please contact dev'
        return 0
      endtry
      return 1
    endif
  endif
endfunction 

" plugin ================
function! s:ip_to_binary(mode)
  let check_result = s:env_check()
  if !check_result
    return
  endif
  normal  `<v`>"sy
  execute 'vne'
  normal v"sp
  let tempname = $TMPDIR."/".fnamemodify(tempname(), ":p:t")
  execute 'w '.tempname
  " warning error will not be outputed
    if a:mode == 'f'
      call system(g:ip_analyzer_virtual_python_path." ".g:ip_analyzer_plugin_path."/ip_to_binary.py ".tempname)
    else
      call system(g:ip_analyzer_virtual_python_path." ".g:ip_analyzer_plugin_path."/binary_to_ip.py ".tempname)
    endif
  endif
  execute 'e!'
  execute 'normal gg00vG$"sy'
  execute 'bd'

  normal `<v`>"sP
  let @s="" "clean register
endfunction 
"" sort by date (my custom sort function)
:command! -nargs=* -range IpToBinary call s:ip_to_binary('f')
:command! -nargs=* -range BinaryToIp call s:ip_to_binary('b')

" IpAnalyzeCIDR
" 192.168.100.14/22 => gatwaay, start from, up to, subnet size, host size 
    " - 11000000.10101000.01100100.00001110 => 192.168.100.14 == the ip
    " - 11111111.11111111.11111100.00000000 => the subnet mask 22
    " - 11000000.10101000.011001**.******** => available ip
    " - 11000000.10101000.01100100.00000001 => gateway (192.168.100.1)
    " - 11000000.10101000.01100100.00000000 => first ip of this subnet (192.168.100.0)
    " - 11000000.10101000.01100111.11111111 => last ip of this subnet (192.168.103.255)
    " - subnet size
function! s:ip_analyze_cidr()
  let check_result = s:env_check()
  if !check_result
    return
  endif
  normal  `<v`>"sy
  execute 'vne'
  normal v"sp
  let tempname = $TMPDIR."/".fnamemodify(tempname(), ":p:t")
  execute 'w '.tempname
  " warning error will not be outputed
  call system(g:ip_analyzer_virtual_python_path." ".g:ip_analyzer_plugin_path."/ip_analyze_cidr.py ".tempname)
  execute 'e!'
  execute 'normal gg00vG$"sy'
  execute 'bd'
  execute 'vne'
  let message = @s
  setlocal buftype=nofile bufhidden=wipe noswapfile nobuflisted nomodified
  silent put=message

  let @s="" "clean register
endfunction 
"" sort by date (my custom sort function)
:command! -nargs=* -range IpAnalyzeCIDR call s:ip_analyze_cidr()
