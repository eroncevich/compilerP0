.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $28, %esp
	movl $5, %eax
	movl $1, %eax
	movl $4, %esi
	movl $8, -12(%ebp)
	movl $12, -16(%ebp)
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	movl $20, %eax
	movl $24, %ebx
	movl $28, -20(%ebp)
	movl $32, %eax
	movl $36, %eax
	movl $40, -8(%ebp)
	movl $44, -4(%ebp)
	movl $48, %edi
	pushl %esi
	call print_any
	popl %esi
	movl %esi, -28(%ebp)
	movl %ebx, -24(%ebp)
	movl -28(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then0
	movl -28(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then1
	movl $777777, %eax
	jmp end1
	then1:
	pushl -28(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -24(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-28(%ebp)
	pushl -28(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end1:
	movl %eax, %eax
	jmp end0
	then0:
	movl -28(%ebp), %ebx
	sarl $2, %ebx
	movl -24(%ebp), %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end0:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -24(%ebp)
	movl -12(%ebp), %eax
	movl %eax, -28(%ebp)
	movl -24(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then2
	movl -24(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then3
	movl $777777, %eax
	jmp end3
	then3:
	pushl -24(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -28(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-24(%ebp)
	pushl -24(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end3:
	movl %eax, %eax
	jmp end2
	then2:
	movl -24(%ebp), %eax
	sarl $2, %eax
	movl -28(%ebp), %ecx
	sarl $2, %ecx
	movl %eax, %ebx
	addl %ecx, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end2:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -24(%ebp)
	movl -20(%ebp), %eax
	movl %eax, -28(%ebp)
	movl -24(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then4
	movl -24(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then5
	movl $777777, %eax
	jmp end5
	then5:
	pushl -24(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -28(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-24(%ebp)
	pushl -24(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end5:
	movl %eax, %eax
	jmp end4
	then4:
	movl -24(%ebp), %ebx
	sarl $2, %ebx
	movl -28(%ebp), %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end4:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -24(%ebp)
	movl -16(%ebp), %eax
	movl %eax, -28(%ebp)
	movl -24(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then6
	movl -24(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then7
	movl $777777, %eax
	jmp end7
	then7:
	pushl -24(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -28(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-24(%ebp)
	pushl -24(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end7:
	movl %eax, %eax
	jmp end6
	then6:
	movl -24(%ebp), %ebx
	sarl $2, %ebx
	movl -28(%ebp), %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end6:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -24(%ebp)
	movl -12(%ebp), %eax
	movl %eax, -12(%ebp)
	movl -24(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then8
	movl -24(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then9
	movl $777777, %eax
	jmp end9
	then9:
	pushl -24(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -12(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-24(%ebp)
	pushl -24(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end9:
	movl %eax, %eax
	jmp end8
	then8:
	movl -24(%ebp), %ebx
	sarl $2, %ebx
	movl -12(%ebp), %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end8:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -12(%ebp)
	movl -20(%ebp), %eax
	movl %eax, -20(%ebp)
	movl -12(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then10
	movl -12(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then11
	movl $777777, %eax
	jmp end11
	then11:
	pushl -12(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -20(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-12(%ebp)
	pushl -12(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end11:
	movl %eax, %eax
	jmp end10
	then10:
	movl -12(%ebp), %eax
	sarl $2, %eax
	movl -20(%ebp), %ecx
	sarl $2, %ecx
	movl %eax, %ebx
	addl %ecx, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end10:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -12(%ebp)
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, -20(%ebp)
	movl -12(%ebp), %eax
	movl %eax, -24(%ebp)
	movl -20(%ebp), %eax
	movl %eax, -20(%ebp)
	movl -24(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then12
	movl -24(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then13
	movl $777777, %eax
	jmp end13
	then13:
	pushl -24(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -20(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-24(%ebp)
	pushl -24(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end13:
	movl %eax, %eax
	jmp end12
	then12:
	movl -24(%ebp), %ebx
	sarl $2, %ebx
	movl -20(%ebp), %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end12:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -20(%ebp)
	movl -16(%ebp), %eax
	movl %eax, -16(%ebp)
	movl -20(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then14
	movl -20(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then15
	movl $777777, %eax
	jmp end15
	then15:
	pushl -20(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -16(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-20(%ebp)
	pushl -20(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end15:
	movl %eax, %eax
	jmp end14
	then14:
	movl -20(%ebp), %ebx
	sarl $2, %ebx
	movl -16(%ebp), %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end14:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -16(%ebp)
	movl -8(%ebp), %eax
	movl %eax, -8(%ebp)
	movl -16(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then16
	movl -16(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then17
	movl $777777, %eax
	jmp end17
	then17:
	pushl -16(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -8(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-16(%ebp)
	pushl -16(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end17:
	movl %eax, %eax
	jmp end16
	then16:
	movl -16(%ebp), %ebx
	sarl $2, %ebx
	movl -8(%ebp), %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end16:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -8(%ebp)
	movl -4(%ebp), %eax
	movl %eax, -4(%ebp)
	movl -8(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then18
	movl -8(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then19
	movl $777777, %eax
	jmp end19
	then19:
	pushl -8(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -4(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-8(%ebp)
	pushl -8(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end19:
	movl %eax, %eax
	jmp end18
	then18:
	movl -8(%ebp), %eax
	sarl $2, %eax
	movl -4(%ebp), %ecx
	sarl $2, %ecx
	movl %eax, %ebx
	addl %ecx, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end18:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -4(%ebp)
	movl %edi, %edi
	movl -4(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then20
	movl -4(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then21
	movl $777777, %eax
	jmp end21
	then21:
	pushl -4(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %edi
	call project_big
	addl $4, %esp
	movl %eax,-4(%ebp)
	pushl -4(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end21:
	movl %eax, %eax
	jmp end20
	then20:
	movl -4(%ebp), %ebx
	sarl $2, %ebx
	movl %edi, %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end20:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -16(%ebp)
	movl -12(%ebp), %edi
	movl %esi, %esi
	movl %edi, %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then22
	movl %edi, %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then23
	movl $777777, %eax
	jmp end23
	then23:
	pushl %edi
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %esi
	call project_big
	addl $4, %esp
	movl %eax,%edi
	pushl %edi
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end23:
	movl %eax, %eax
	jmp end22
	then22:
	movl %edi, %ebx
	sarl $2, %ebx
	movl %esi, %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end22:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -16(%ebp)
	movl -16(%ebp), %esi
	pushl -16(%ebp)
	call print_any
	popl -16(%ebp)
	movl $0,%eax
	leave
	ret
