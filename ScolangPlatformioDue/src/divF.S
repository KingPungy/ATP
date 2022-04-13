.cpu cortex-m0
.align 2

.text
.global divF

divF:
push { r4, r5, lr }
mov r4, r0
mov r5, r1
mov r0, r4
mov r1, r5
bl divide
mov r4, r0
mov r0, r4
pop { r4, r5, pc }
