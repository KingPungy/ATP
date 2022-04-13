.cpu cortex-m0
.align 2

.text
.global smartPrint

smartPrint:
push { r4, lr }
mov r4, r0
ldr r1, =536870912 @ 0x20000000 start of data segment
cmp r0, r1
bls isInt

mov r0, r4
bl printlnStr
b End

isInt:
mov r0, r4
bl printlnInteger

End:
pop { r4, pc }
