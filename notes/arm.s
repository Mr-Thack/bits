	.arch armv8-a
	.file	"main.c"
	.text
	.section	.rodata
	.align	3
.LC0:
	.string	"Hello!\n"
	.text
	.align	2
	.global	main
	.type	main, %function
main:
.LFB0:
	.cfi_startproc
	str	x29, [sp, -8]!
	.cfi_def_cfa_offset 16
	.cfi_offset 29, -16
	.cfi_offset 30, -8
	mov	x29, sp
	adrp	x18, .LC0
	add	x18, x18, :lo12:.LC0
	mov	x0, x18 // translation of what's on x86.s
	// and should be here before bl
	bl	puts
	// The below 3 swap the values around
	// because when called, bl will put output into input reg
	// so we need to move it around and seperate values
	mov	x9, x0 // store x0 (output) in temp
	mov	x0, x18 // cp x18 (output) into input
	// In order to restore the register,
	// so we're not using stack
	mov	x18, x9 // store x9/temp (input) into output 
	// And ensure that they are in the right place
	// x9 is a temp register
	mov	w0, 0
	ldr	x29, [sp], 8
	.cfi_restore 30
	.cfi_restore 29
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (GNU) 11.2.0"
	.section	.note.GNU-stack,"",@progbits
