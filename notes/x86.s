	.file	"main.c"
	.text
	.section	.rodata
.LC0:
	.string	"Hello!\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	; register x29 AKA fp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	; registers x29 and sp 
	.cfi_def_cfa_register 6
	; leaq whatever this is,
	; is translated to: 
	; adrp x0, .LC0
	; add x0, x0, :lo12:.LC0
	leaq	.LC0(%rip), %rax
	; We're not even going to use rip
	; We'll use adrp instead of leaq which will do that automatically
	; ISSUE rax is a temp reg, but also 1st output
	; Where as r0 is 1st in and out
	; We could try pushing RAX before sys int
	; then we could do a "mov r18, r0"
	; because r18 is last temp reg
	; and we're probably not going to be using it
	; due to x64 only keeping 4 temp regs
	movq	%rax, %rdi
	; The extra move is copying RAX into RDI
	; is probably happening because this was compiled using -01
	; instead of -03
	; I'd expect gcc to optimize it properly when compiled properly
	call	puts@PLT
	; Don't know what the @PLT is for, but seems to be a comment
	movl	$0, %eax
	; eax is w0
	popq	%rbp
	; also easy to implement
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (GNU) 11.1.0"
	.section	.note.GNU-stack,"",@progbits
