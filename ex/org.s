.intel_syntax noprefix
.section .text
.globl main
main:
	push RBP
	mov RBP, RSP
	lea RAX, QWORD PTR [RIP+.L_2004]
	mov RDI, RAX
	call puts@PLT
	mov EAX, 0
	pop RBP
	ret
.section .rodata
.L_2004:
	.string "Hello!"
