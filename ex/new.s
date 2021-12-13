.section .text
.global main
main:
	#str x29,[x29]
	#mov x29,x30
	#adrp x0, .L_2004
	#add x0, x0, .L_2004
	
	#stp     x29, x30, [sp, -16]!
        #mov     x29, sp
        adrp    x0, .L_2004
        add     x0, x0, :lo12:.L_2004
	bl puts
	mov w0, 0
	ldr x29, [x29]
	ret
.section .rodata
.L_2004:
	.string "Hello!"

