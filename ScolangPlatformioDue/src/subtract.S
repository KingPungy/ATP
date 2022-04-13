.cpu cortex-m0
.align 2

.text
.global subtract

subtract:
push { r4, r5, lr }
mov r4, r0
mov r5, r1
sub r4, r4, r5
mov r0, r4
pop { r4, r5, pc }
